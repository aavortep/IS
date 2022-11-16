import random
import math
from base64 import b32encode, b32decode


n_prime = 1000


def read_file(filename):
    f = open(filename, 'rb')
    data = b32encode(f.read())
    msg = data.decode("ascii")  # декодирование строки байтов в строковый объект
    f.close()
    return msg


def write_file(filename, msg):
    f = open(filename, 'wb')
    data = b32decode(msg)
    f.write(data)
    f.close()
    return data


# решето Эратосфена
def eratosfen():
    primes = [i for i in range(n_prime + 1)]
    primes[1] = 0  # 0 обозначает составное число
    for i in range(2, n_prime + 1):
        if primes[i] != 0:
            for k in range(2 * i, n_prime + 1, i):
                primes[k] = 0
    primes = set(primes)  # удаление всех составных чисел (кроме одного)
    primes.remove(0)  # удаление оставшегося составного числа
    primes = list(primes)
    primes.sort()
    primes = primes[len(primes)//2:]
    return primes


# расширенный алгоритм Евклида (x * a + y * b = НОД)
def ext_euclid(a, b):
    x, y, c, d = 1, 0, 0, 1  # первая матрица Е
    while b:
        q = a // b
        a, b = b, a % b
        x, y = y, x - q * y  # умножение Е на матрицу [[0, 1], [1, -q]]
        c, d = d, c - q * d
    return a, x, y  # a - искомый НОД


# открытый ключ
def get_e(fi):
    e = random.randint(0, fi)
    gcd, x, y = ext_euclid(fi, e)
    while gcd != 1:
        e = random.randint(0, fi)
        gcd, x, y = ext_euclid(fi, e)
    return e


# секретный ключ
def get_d(e, fi):
    k = 0
    while (k * fi + 1) % e != 0:
        k += 1
    return (k * fi + 1) // e


def rsa_params():
    p = random.choice(eratosfen())
    q = random.choice(eratosfen())
    n = p * q  # длина алфавита
    fi = (p - 1) * (q - 1)  # функция Эйлера
    e = get_e(fi)
    d = get_d(e, fi)
    return n, e, d


def encipher(msg, n, e):
    res = ""
    for symb in msg:
        ch = pow(ord(symb), e, n)  # возведение в степень по модулю
        res += str(ch) + " "
    res = res[:-1]
    return res


def decipher(msg, n, d):
    res = ""
    msg = msg.split()
    for symb in msg:
        ch = pow(int(symb), d, n)
        res += chr(ch)
    return res


if __name__ == '__main__':
    filename = input("Введите название файла: ")
    msg = read_file(filename)

    n, e, d = rsa_params()
    encipher_msg = encipher(msg, n, e)
    print("Зашифрованное сообщение: " + encipher_msg)
    f = open("enc_" + filename, 'w')
    f.write(encipher_msg)
    f.close()

    flag = input("Расшифровать сообщение? (y - да, n - нет):  ")
    if flag == "y":
        decipher_msg = decipher(encipher_msg, n, d)
        data = write_file("enc_" + filename, decipher_msg)
        print("Расшифрованное сообщение: ", data)
