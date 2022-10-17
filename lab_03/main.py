from bitarray import bitarray


def read_file(filename):
    f = open(filename, 'rb')
    msg = ''
    for line in f:
        msg += "".join(map(chr, line))  # декодирование строки байтов в строковый объект
    f.close()
    return msg


def write_file(filename, msg):
    f = open(filename, 'wb')
    for symb in msg:
        bt = symb.encode('ISO-8859-1')  # кодирование строки в байты
        f.write(bt)
    f.close()


def replace(msg):
    for i in range(len(msg)):
        if msg[i] == "11011010":
            msg[i] = "00001010"
    return msg


# Преобразование строки в двоичный код
def bit_encode(s: str):
    to_hex = ''
    for c in s.encode('utf-8'):
        hexed = hex(c)[2:]
        if len(hexed) == 1:
            hexed = '0' + hexed
        to_hex += hexed
    to_bin = ''.join([bin(int('1' + to_hex, 16))[3:]])
    return bitarray(to_bin).to01()


# Преобразование двоичного кода в строку
def bit_decode(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s]])


#  Разделить строку на группы по 64 бит
def split_encode_input(enter):
    result = []
    bit_string = bit_encode(enter)
    # Если длина не делится на 64, добавить нули
    if len(bit_string) % 64 != 0:
        for i in range(64 - len(bit_string) % 64):
            bit_string += '0'
    for i in range(len(bit_string) // 64):
        result.append(bit_string[i * 64: i * 64 + 64])
    return result


#  Разбить 16-ричную строку на блоки по 64 бит
def split_decode_input(enter):
    result = []
    input_list = enter.split("0x")[1:]
    int_list = [int("0x" + i, 16) for i in input_list]
    for i in int_list:
        bin_data = str(bin(i))[2:]
        while len(bin_data) < 64:
            bin_data = '0' + bin_data
        result.append(bin_data)
    return result


# перестановки
def permutation(enter, table):
    result = ""
    for i in table:
        result += enter[i - 1]
    return result


# перестановка В
def key_permutation(key):
    key = bit_encode(key)
    while len(key) < 64:
        key += '0'
    table = (57, 49, 41, 33, 25, 17, 9,
             1, 58, 50, 42, 34, 26, 18,
             10, 2, 59, 51, 43, 35, 27,
             19, 11, 3, 60, 52, 44, 36,
             63, 55, 47, 39, 31, 23, 15,
             7, 62, 54, 46, 38, 30, 22,
             14, 6, 61, 53, 45, 37, 29,
             21, 13, 5, 28, 20, 12, 4)
    return permutation(key, table)


# сжимающая перестановка СР
def compress_key(key):
    table = (14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4,
             26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40,
             51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32)
    return permutation(key, table)


# сдвиги ключей
def shift_key(key):
    c0 = key[:28]
    d0 = key[28:]
    shift_table = (1, 2, 4, 6, 8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 27, 28)
    round_keys = []
    for i in range(16):
        c0_shift = c0[shift_table[i]:] + c0[:shift_table[i]]
        d0_shift = d0[shift_table[i]:] + d0[:shift_table[i]]
        key48 = compress_key(c0_shift + d0_shift)
        round_keys.append(key48)
    return round_keys


# генерация раундовых ключей
def gen_keys(key64):
    key56 = key_permutation(key64)
    res_keys = shift_key(key56)
    return res_keys


# расширяющая перестановка Е
def extend_perm(msg):
    table = (32, 1, 2, 3, 4, 5,
             4, 5, 6, 7, 8, 9,
             8, 9, 10, 11, 12, 13,
             12, 13, 14, 15, 16, 17,
             16, 17, 18, 19, 20, 21,
             20, 21, 22, 23, 24, 25,
             24, 25, 26, 27, 28, 29,
             28, 29, 30, 31, 32, 1)
    return permutation(msg, table)


def xor(a, b):
    result = ""
    for i in range(len(a)):
        result += '0' if a[i] == b[i] else '1'
    return result


# замена с помощью s-блоков
def s_block_replace(msg48):
    s_block_table = (
        (
            (14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7),
            (0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8),
            (4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0),
            (15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13),
        ),
        (
            (15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10),
            (3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5),
            (0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15),
            (13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9),
        ),
        (
            (10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8),
            (13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1),
            (13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7),
            (1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12),
        ),
        (
            (7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15),
            (13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9),
            (10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4),
            (3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14),
        ),
        (
            (2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9),
            (14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6),
            (4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14),
            (11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3),
        ),
        (
            (12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11),
            (10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8),
            (9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6),
            (4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13),
        ),
        (
            (4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1),
            (13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6),
            (1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2),
            (6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12),
        ),
        (
            (13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7),
            (1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2),
            (7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8),
            (2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11),
        )
    )
    msg32 = ""
    for i in range(8):
        row_bit = (msg48[i * 6] + msg48[i * 6 + 5]).encode("utf-8")
        col_bit = (msg48[i * 6 + 1:i * 6 + 5]).encode("utf-8")
        row = int(row_bit, 2)
        col = int(col_bit, 2)
        data = s_block_table[i][row][col]
        res = str(bin(data))[2:]
        while len(res) < 4:
            res = '0' + res
        msg32 += res
    return msg32


# перестановка P
def feistel_perm(msg32):
    table = (16, 7, 20, 21,
             29, 12, 28, 17,
             1, 15, 23, 26,
             5, 18, 31, 10,
             2, 8, 24, 14,
             32, 27, 3, 9,
             19, 13, 30, 6,
             22, 11, 4, 25)
    return permutation(msg32, table)


# шифр Фейстеля
def feistel(msg32, key):
    msg48 = extend_perm(msg32)
    s_block_res = s_block_replace(xor(msg48, key))
    return feistel_perm(s_block_res)


# начальная перестановка IP
def init_perm(msg64):
    table = (58, 50, 42, 34, 26, 18, 10, 2,
             60, 52, 44, 36, 28, 20, 12, 4,
             62, 54, 46, 38, 30, 22, 14, 6,
             64, 56, 48, 40, 32, 24, 16, 8,
             57, 49, 41, 33, 25, 17, 9, 1,
             59, 51, 43, 35, 27, 19, 11, 3,
             61, 53, 45, 37, 29, 21, 13, 5,
             63, 55, 47, 39, 31, 23, 15, 7)
    return permutation(msg64, table)


# конечная перестановка IP^(-1)
def end_perm(msg64):
    table = (40, 8, 48, 16, 56, 24, 64, 32,
             39, 7, 47, 15, 55, 23, 63, 31,
             38, 6, 46, 14, 54, 22, 62, 30,
             37, 5, 45, 13, 53, 21, 61, 29,
             36, 4, 44, 12, 52, 20, 60, 28,
             35, 3, 43, 11, 51, 19, 59, 27,
             34, 2, 42, 10, 50, 18, 58, 26,
             33, 1, 41, 9, 49, 17, 57, 25)
    return permutation(msg64, table)


def encipher(msg, keys):
    result = ""
    blocks64 = split_encode_input(msg)
    print(blocks64)
    for block in blocks64:
        print("=====================")
        print("Блок текста до шифровки: ", block)
        ip_res = init_perm(block)
        print("Начальная перестановка: ", ip_res)
        left, right = ip_res[:32], ip_res[32:]
        for i in range(16):
            print("------------------------")
            print("Ключ: ", keys[i])
            new_left = right
            new_right = xor(left, feistel(right, keys[i]))
            print("Фейстель: ", feistel(right, keys[i]))
            left = new_left
            right = new_right
            print("Новая левая половина: ", left)
            print("Новая правая половина: ", right)
        print("------------------------")
        block_result = right + left
        block_result = end_perm(block_result)
        print("Конечная перестановка: ", block_result)
        result += str(hex(int(block_result.encode(), 2)))
    print("=====================")
    return result


def decipher(msg, keys):
    result = []
    blocks64 = split_decode_input(msg)
    #blocks64 = []
    #for i in range(len(msg) // 64):
        #blocks64.append(msg[i * 64: i * 64 + 64])
    for block in blocks64:
        print("=====================")
        print("Блок текста до расшифровки: ", block)
        ip_res = init_perm(block)
        print("Начальная перестановка: ", ip_res)
        left, right = ip_res[:32], ip_res[32:]
        for i in range(15, -1, -1):
            print("------------------------")
            print("Ключ: ", keys[i])
            new_left = right
            new_right = xor(left, feistel(right, keys[i]))
            print("Фейстель: ", feistel(right, keys[i]))
            left = new_left
            right = new_right
            print("Новая левая половина: ", left)
            print("Новая правая половина: ", right)
        print("------------------------")
        block_result = right + left
        block_result = end_perm(block_result)
        print("Конечная перестановка: ", block_result)
        for i in range(0, len(block_result), 8):
            result.append(block_result[i: i + 8])
    print("=====================")
    print("Двоичная расшифровка: ", result)
    #result = replace(result)
    while result[-1] == "00000000":
        result.pop()
    decoded = bit_decode(result)
    return decoded


if __name__ == '__main__':
    key = "petrova"
    filename = input("Введите название файла: ")
    msg = read_file(filename)

    keys = gen_keys(key)

    encipher_msg = encipher(msg, keys)
    print("Зашифрованное сообщение: " + encipher_msg)
    write_file(filename, encipher_msg)

    flag = input("Расшифровать сообщение? (y - да, n - нет):  ")
    if flag == "y":
        msg = read_file(filename)
        decipher_msg = decipher(msg, keys)
        write_file(filename, decipher_msg)
        print("Расшифрованное сообщение: ", decipher_msg)
