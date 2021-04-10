from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
# from server.encryptionDES import checkDES_Key
import ARappServer.DBinterface as DBi

RSA_PRIVATE_KEY = 'privatekey.pem'


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


def checkRSA_PrivateKey():
    '''
    Проверка на наличие ключа DES KEY
    :return:
    '''
    try:
        if not open(RSA_PRIVATE_KEY).read():
            raise WrongRSA_Key(RSA_PRIVATE_KEY)  # TODO обработать отсутствие данных в ключе
    except:
        raise WrongRSA_Key(RSA_PRIVATE_KEY)


##########################################################

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
    result = DBi.User_DB.getNamefromlogin(login, password_decode)
    return result


# if __name__ == '__main__':
#     # collection_names = "radiator"
#     # # while True:
#     # aa = getMany(collection_names, {}, 110)
#     # print(aa)
#     # #     if not aa['n']: break
#     # print(getLastOne("radiator"))
#     # print(help(deleteOne(collection_names,{"id":4})))
#
#     # DB = BaseDBinterface(client.ARdb)
#     DB1 = User_DB(client.UserDB)
#
        # print(DBi.User_DB.getNamefromlogin("TEST", "TEST0912375981237059812730"))
#     print(DB1.getLastId('users'))
