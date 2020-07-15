from Cryptodome.Cipher import DES
from Crypto.Util.Padding import pad, unpad

# from Cryptodome.PublicKey import RSA
import rsa
from server import DBinterface as iDB

from Crypto.Cipher import PKCS1_OAEP
# from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

BLOCK_SIZE = 16
file = open("Key.txt", "rb")
key = (file.read())
file.close()


# def pad(text):
#     print("pad")
#     while len(text) % 8 != 0:
#         text += b''
#         print(text)
#     return text


# coding password
def coding(password):
    des = DES.new(key, DES.MODE_ECB)
    test_string = password
    #print("pass: ", test_string)
    text = test_string.encode('utf8')
    print("text",text)
    # text = bytes(test_string,'utf-8')
    padded_text = pad(text,BLOCK_SIZE)
    # padded_text = text
    print("padded_text ", padded_text)
    encrypted_text = des.encrypt(padded_text)
    print("encrypted_text",encrypted_text)
    return encrypted_text


# дешифровка
def decoding(name):
    des = DES.new(key, DES.MODE_ECB)
    data = des.decrypt(name)
    data = data.decode('utf-8')
    print("data",data)
    return data


def authen(login, password):
    key = RSA.importKey(open('privatekey.pem').read())
    cipher = PKCS1_OAEP.new(key)
    # cipher = PKCS1_v1_5.new(key)
    message = cipher.decrypt(password)
    print("messagewq ",message.decode())

    # key = RSA.generate(2048)
    # encrypted_key = key.exportKey()
    # with open('privatekey.pem', 'wb') as f:
    #    f.write(encrypted_key)
    # with open('publickey.pem', 'wb') as f:
    #    f.write(key.publickey().exportKey())
    # privkey = rsa.PrivateKey.load_pkcs1(open('privatekey.pem', 'rb').read())
    # # print(privkey)
    # # print(password)
    # # print(login)
    # # pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(open('publickey.pem', 'rb').read())
    # # message = password.encode('utf8')
    # # crypto = rsa.encrypt(message, pubkey)
    # # расшифровка клиентского пароля
    # message = rsa.decrypt(password, privkey)
    message = message.decode()
    a = iDB.getNamefromlogin(login, message)
    return a
