from Cryptodome.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from server import DBinterface as iDB

BLOCK_SIZE = 16


class FileEmpty(Exception):
    def __init__(self, *args):
        self.message = "There is not DSA-encryption key in the file 'Key.txt'"

    def __str__(self):
        if self.message:
            return 'FileEmpty, {0} '.format(self.message)
        else:
            return 'FileEmpty has been raised'

class WrongKey(Exception):
    def __init__(self, *args):
        self.message = "There is changed DSA-encryption key in the file 'Key.txt'" \
                       "\nChange DSA-encryption key or rewrite all users (including the base user) in database."

    def __str__(self):
        if self.message:
            return 'WrongKey, {0} '.format(self.message)
        else:
            return 'WrongKey has been raised'

try:
    file = open("Key.txt", "rb")
    if not open("Key.txt", "rb").read():
        raise FileEmpty
    key = (file.read())
    file.close()
except FileNotFoundError:
    file = open("Key.txt", "wb")
    print("No such file: 'Key.txt'")
    raise FileEmpty

result = iDB.getNamefromlogin("TEST", "TEST0912375981237059812730")
if result == "Incorrect login or password":
    raise WrongKey

def coding(password):
    '''
    Шифрование пароля, для хранения в базе данных
    Шифрование производится алгоритмом DES
    RFC 4772 (https://www.rfc-editor.org/rfc/rfc4772.txt)
    :param password: <class 'str'> пароль !!! в незашифрованном виде
    :return: <class 'bytes'> зашифрованный пароль
    '''
    des = DES.new(key, DES.MODE_ECB)
    password_encoded = password.encode('utf8')
    padded_password = pad(password_encoded, BLOCK_SIZE)
    encrypted_password = des.encrypt(padded_password)
    return encrypted_password


# # дешифровка
# def decoding(password):
#     '''
#     Дештифрование пароля
#     :param name: password
#     :return:
#     '''
#     des = DES.new(key, DES.MODE_ECB)
#     data = des.decrypt(password)
#     data = data.decode('utf-8')
#     print("data", data)
#     return data


def authen(login, password):
    '''
    Производится аутентификация пользователя по логину и паролю.
    Шифрование производится алгоритмом  RSA-OAEP
    RFC 2437 (https://tools.ietf.org/html/rfc2437)
    :param login: <class 'str'> Логин пользователя
    :param password: <class 'bytes'> зашифрованный пароль в представлении
            последовательности байтов
    :return: <class 'str'> Возвращается резщультат аутентификации:
            "Successful authentication." or "Incorrect login or password."
    '''
    key = RSA.importKey(open('privatekey.pem').read())
    cipher = PKCS1_OAEP.new(key)
    password_decrypt = cipher.decrypt(password)
    password_decode = password_decrypt.decode()
    result = iDB.getNamefromlogin(login, password_decode)
    return result
