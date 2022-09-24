import random

size = 256


def read_file(filename):
    f = open(filename, 'rb')
    msg = ''
    for line in f:
        msg += line.decode('ISO-8859-1')  # декодирование строки байтов в строковый объект
    f.close()
    return msg


def write_file(filename, msg):
    f = open(filename, 'wb')
    for symb in msg:
        bt = symb.encode('ISO-8859-1')  # кодирование строки в байты
        f.write(bt)
    f.close()


def new_rotor():
    rotor = [i for i in range(size)]
    random.shuffle(rotor)  # перемешивание
    return rotor


def new_reflector():
    reflector = [None for _ in range(size)]
    mas = [x for x in range(size)]
    for i in range(size):
        if reflector[i] is None:
            num = random.choice(mas)
            while num == i:
                num = random.choice(mas)
            mas.pop(mas.index(num))
            mas.pop(mas.index(i))
            reflector[i] = num
            reflector[num] = i
    return reflector


def encipher(s, rotor1, rotor2, rotor3, reflector):  # шифрование одного символа
    # прямой ход
    s1 = rotor1.index(s)
    s2 = rotor2.index(s1)
    s3 = rotor3.index(s2)

    s4 = reflector[s3]

    # обратный ход
    s5 = rotor3[s4]
    s6 = rotor2[s5]
    s7 = rotor1[s6]
    return s7


def encipher_message(msg, rotor1, rotor2, rotor3, reflector):
    nums = [ord(c) for c in msg]  # перевод строки символов в массив чисел
    res_msg = []
    shift1 = 0
    shift2 = 0
    shift3 = 0
    for s in nums:
        res_msg.append(encipher(s, rotor1, rotor2, rotor3, reflector))

        # поворот роторов
        if shift1 < size:
            rotor1 = rotor1[1:] + rotor1[:1]
            shift1 += 1
        elif shift2 < size:
            rotor1 = rotor1[1:] + rotor1[:1]
            rotor2 = rotor2[1:] + rotor2[:1]
            shift1 = 0
            shift2 += 1
        elif shift3 < size:
            rotor1 = rotor1[1:] + rotor1[:1]
            rotor2 = rotor2[1:] + rotor2[:1]
            rotor3 = rotor3[1:] + rotor3[:1]
            shift1 = 0
            shift2 = 0
            shift3 += 1
        else:
            rotor1 = rotor1[1:] + rotor1[:1]
            rotor2 = rotor2[1:] + rotor2[:1]
            rotor3 = rotor3[1:] + rotor3[:1]
            shift1 = 0
            shift2 = 0
            shift3 = 0

    return ''.join([chr(c) for c in res_msg])  # перевод массива чисел в строку символов


def main():
    rotor1 = new_rotor()
    rotor2 = new_rotor()
    rotor3 = new_rotor()
    reflector = new_reflector()

    filename = input("Введите название файла: ")
    msg = read_file(filename)

    msg_enigma = encipher_message(msg, rotor1, rotor2, rotor3, reflector)
    print("Зашифрованное сообщение: ", msg_enigma)

    write_file(filename, msg_enigma)
    print("Зашифрованное сообщение записано в файл")

    flag = input("Расшифровать сообщение? (y - да, n - нет):  ")
    if flag == "y":
        msg = read_file(filename)
        msg_secured = encipher_message(msg, rotor1, rotor2, rotor3, reflector)
        write_file(filename, msg_secured)
        print("Расшифрованное сообщение: ", msg_secured)


if __name__ == '__main__':
    main()
