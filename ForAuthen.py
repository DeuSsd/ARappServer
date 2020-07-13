from Cryptodome.Cipher import DES
from Cryptodome.PublicKey import RSA
import rsa
from server import DBinterface as iDB

file = open("Key.txt", "rb")
key = (file.read())
file.close()
def pad(text):
    while len(text) % 8 != 0:
           text += b' '
    return text
#coding password
def coding(password):
    des = DES.new(key, DES.MODE_ECB)
    test_string = password
    text = bytes(test_string, 'utf8')
    padded_text = pad(text)
    encrypted_text = des.encrypt(padded_text)
    print(encrypted_text)
    return encrypted_text
#дешифровка
def decoding(name):
    des = DES.new(key, DES.MODE_ECB)
    data = des.decrypt(name)
    data=data.decode('utf8')
    print(data)
    return data

def authen(login, password):
    #key = RSA.generate(2048)
    #encrypted_key = key.exportKey()
    #with open('privatekey.pem', 'wb') as f:
    #    f.write(encrypted_key)
    #with open('publickey.pem', 'wb') as f:
    #    f.write(key.publickey().exportKey())
    privkey = rsa.PrivateKey.load_pkcs1(open('privatekey.pem', 'rb').read())
    print(privkey)
    print(password)
    print(login)
    #pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(open('publickey.pem', 'rb').read())
    #message = password.encode('utf8')
    #crypto = rsa.encrypt(message, pubkey)
    #расшифровка клиентского пароля
    message = rsa.decrypt(password, privkey)
    message = message.decode('utf8')
    print(message)
    a = iDB.getNamefromlogin(login, message)
    return a
