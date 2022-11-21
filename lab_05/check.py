from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15  # схема цифровой подписи на основе RSA


def check_signature(data):
    hash = SHA256.new(data)

    public_key_file = open('public_key.txt', 'rb')
    public_key = RSA.import_key(public_key_file.read())

    signature = open('signature.txt', 'rb').read()

    try:
        pkcs1_15.new(public_key).verify(hash, signature)  # проверка подписи (расшифровка)
        print("Проверка подписи успешно пройдена")
    except (ValueError, TypeError):
        print("Проверка подписи НЕ пройдена!")


if __name__ == '__main__':
    with open("positive_test.pdf", 'rb') as input_file:
        data = input_file.read()
        check_signature(data)
