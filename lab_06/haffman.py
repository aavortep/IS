import pickle


def read_file(filename):
    f = open(filename, 'rb')
    msg = f.read()
    f.close()
    return msg


def write_file(filename, msg):
    f = open(filename, 'wb')
    for symb in msg:
        bt = symb.encode('ISO-8859-1')  # кодирование строки в байты
        f.write(bt)
    f.close()


def make_freq_table(data):
    table = {}
    for char in data:
        if char in table:
            freq = table[char]
        else:
            freq = 0
        table.update([(char, freq + 1)])
    return table


def is_leaf(node):
    return node.left is None and node.right is None


class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):  # для сравнения двух узлов (lower than)
        return self.freq < other.freq


def insert_in_queue(queue, node):
    j = 0
    while j < len(queue) and node < queue[j]:
        j += 1
    queue.insert(j, node)
    return queue


def make_tree(freq_table):
    # создание очереди приоритетов по частоте символов
    chars = list(freq_table.keys())
    queue = [Node(chars[0], freq_table[chars[0]])]
    # добавление всех символов в дерево в качестве листьев
    for i in range(1, len(chars)):
        ch = chars[i]
        new_leaf = Node(ch, freq_table[ch])
        queue = insert_in_queue(queue, new_leaf)

    while len(queue) > 1:
        # два символа с наименьшей частотой
        left = queue.pop()
        right = queue.pop()
        # новый внутренний узел
        new_node = Node(None, left.freq + right.freq, left, right)
        queue = insert_in_queue(queue, new_node)

    root = queue[0]  # корень дерева
    return root


# проход по дереву Хаффмана и сохранение кодов в словаре
def encode(root, s, huffman_code):
    if root is None:
        return

    if is_leaf(root):
        huffman_code[root.char] = s if len(s) > 0 else '1'

    encode(root.left, s + '1', huffman_code)
    encode(root.right, s + '0', huffman_code)


def compress(data, huffman_code):
    binary = ""
    for char in data:
        binary += huffman_code[char]
    res = ""
    for i in range(len(binary) // 8 + 1):
        if i * 8 + 8 <= len(binary):
            res += chr(int(binary[i*8:i*8+8], 2))
        else:
            res += chr(int(binary[i * 8:], 2))
    res += str(len(binary) % 8)  # длина последнего символа в битах (если 0, то он не "обрезан")
    return res


def decompress(data, root, index, res):
    if root is None:
        return index, res

    if is_leaf(root):
        res += chr(root.char)
        return index, res

    index += 1
    root = root.left if data[index] == '1' else root.right
    return decompress(data, root, index, res)


if __name__ == '__main__':
    filename = input("Введите название файла, который надо сжать: ")

    data = read_file(filename)
    table = make_freq_table(data)
    root = make_tree(table)
    pickle.dump(root, open("tree_" + filename, "wb"))  # сохранение дерева в файле
    huffman_code = {}
    encode(root, '', huffman_code)
    compressed = compress(data, huffman_code)
    print(compressed)
    write_file("compressed_" + filename, compressed)

    flag = input("Разжать файл? (y - да, n - нет):  ")
    if flag == "y":
        f = open("compressed_" + filename, 'rb')
        compressed = ''
        for line in f:
            compressed += line.decode('ISO-8859-1')  # декодирование строки байтов в строковый объект
        f.close()

        binary = ""
        for i in range(len(compressed) - 1):
            to_bin = str(bin(ord(compressed[i]))[2:])
            while len(to_bin) < 8:
                to_bin = "0" + to_bin
            binary += to_bin
        # манипуляции с последним байтом
        last_byte_len = int(compressed[-1])  # длина последнего символа
        last_byte = binary[len(binary) - 9:]
        last_byte = last_byte[8 - last_byte_len:]
        binary = binary[:len(binary) - 9] + last_byte
        deserial = pickle.load(open("tree_" + filename, "rb"))  # получение дерева из файла
        index = -1
        decompressed = ""
        while index < len(binary) - 1:
            index, decompressed = decompress(binary, deserial, index, decompressed)
        #print(decompressed)
        write_file("decompressed_" + filename, decompressed)
