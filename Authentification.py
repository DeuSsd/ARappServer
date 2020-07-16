from Cryptodome.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from server import DBinterface as iDB

BLOCK_SIZE = 16
DES_KEY_FILE = 'key.txt'
RSA_PRIVATE_KEY = 'privatekey.pem'
TEST_LOGIN = "TEST"
TEST_PASSWORD = "TEST0912375981237059812730"


# Обработка ошибки отсутствия файла с DES KEY
class FileEmpty(Exception):
    def __init__(self, arg):
        self.message = f"There is not DSA-encryption key in the file '{arg}'"

    def __str__(self):
        if self.message:
            return 'FileEmpty, {0} '.format(self.message)
        else:
            return 'FileEmpty has been raised'


# Обработка ошибки неправильного ключа DES KEY
class WrongDES_Key(Exception):
    def __init__(self, arg):
        self.message = f"There is changed DSA-encryption key in the file '{arg}'" \
                       "\nChange DSA-encryption key or rewrite all users (including the base user) in database."

    def __str__(self):
        if self.message:
            return 'WrongDES_Key, {0} '.format(self.message)
        else:
            return 'WrongDES_Key has been raised'

# Обработка ошибки неправильного ключа DES KEY
class WrongRSA_Key(Exception):
    def __init__(self, arg):
        self.message = f"The file '{arg}' with the private encryption key was not found" \
                       "\nPrivate encryption key not found."

    def __str__(self):
        if self.message:
            return 'WrongRSA_Key, {0} '.format(self.message)
        else:
            return 'WrongRSA_Key has been raised'

def checkDES_Key():
    '''
    Проверка на наличие ключа DES KEY
    :return:
    '''
    if "Incorrect login or password" == iDB.getNamefromlogin(TEST_LOGIN, TEST_PASSWORD):
        raise WrongDES_Key(DES_KEY_FILE)

def checkRSA_PrivateKey():
    '''
    Проверка на наличие ключа DES KEY
    :return:
    '''
    try:
        if not open(RSA_PRIVATE_KEY).read():
            raise WrongRSA_Key(RSA_PRIVATE_KEY) #TODO обработать отсутствие данных в ключе
    except:
        raise WrongRSA_Key(RSA_PRIVATE_KEY)


def checkKeys():
    checkDES_Key()
    checkRSA_PrivateKey()

try:
    file = open(DES_KEY_FILE, "rb")
    if not open(DES_KEY_FILE, "rb").read():
        raise FileEmpty(DES_KEY_FILE)
    key = (file.read())
    file.close()
except FileNotFoundError:
    file = open(DES_KEY_FILE, "wb")
    print(f"No such file: '{DES_KEY_FILE}'")
    raise FileEmpty(DES_KEY_FILE)


##########################################################

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
    key = RSA.importKey(open(RSA_PRIVATE_KEY).read())
    cipher = PKCS1_OAEP.new(key)
    password_decrypt = cipher.decrypt(password)
    password_decode = password_decrypt.decode()
    result = iDB.getNamefromlogin(login, password_decode)
    return result
