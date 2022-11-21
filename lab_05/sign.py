from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15  # схема цифровой подписи на основе RSA


def sign_doc(data):
    hash = SHA256.new(data)  # Хэш-функция от данных из файла
    keys = RSA.generate(2048)  # Генерирация ключей (2048 бит)

    signature = pkcs1_15.new(keys).sign(hash)  # Подписание (шифрование)

    sign_file = open('signature.txt', 'wb')
    sign_file.write(signature)
    sign_file.close()

    public_key = keys.publickey()
    public_key_file = open('public_key.txt', 'wb')
    public_key_file.write(public_key.exportKey())
    public_key_file.close()


if __name__ == '__main__':
    with open("positive_test.pdf", 'rb') as input_file:
        data = input_file.read()
        sign_doc(data)
        print("Электронная подпись поставлена")
