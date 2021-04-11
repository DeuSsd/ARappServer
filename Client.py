
import socket
import rsa
import time
#для шифровки пароля
#pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(open('publickey.pem', 'rb').read())
#message = 'onelove1'.encode('utf8')
#crypto = rsa.encrypt(message, pubkey)
#print(crypto)

# для тестов
msg1 = {
    "method": "get",
    "parametrs": {
        "collectionName": "users",
        "filter": {
            "name": "Denis"
        }
    }
}
msg2 = {
    "method": "delete",
    "parametrs": {
        "collectionName": "radiator",
        "filter": {
            "Temperature": {'$lt': 10}
        }
    }
}
msg3 = {
    "method": "put",
    "parametrs": {
        "collectionName": "radiator",
        "data": {
            "Temperature": 150.256
        }
    }
}
msg5 = {
    "method": "put"
}
msg4 = {
    "method": "get",
    "parametrs": {
        "collectionName": "radiator",
        "filter": {
            "Temperature": {'$gt': 150}
        }
    }
}

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

import base64

messages = b'qwer1ty12'
key = RSA.importKey(open('publickey.pem').read())
print()
cipher = PKCS1_OAEP.new(key)
ciphertext = cipher.encrypt(messages)

msg6 = {
    "method": "logIn",
    "parametrs": {
        # "collectionName": "users",
        "name": "Roman",
        "password": base64.b64encode(ciphertext).decode()
        # "password": ciphertext
        # "password": "BKxpVOz40cf+AvStNcgNEmpBUCq2NG   BMYtHvI+W8h6QJ3KDy4WryD+/c8pouLikq3Qa3CNPlrMPIGxK+o4uO6O8kqFN/LARoNVDMRamG+JI1bdnZ0fUsCaNQZ4tlBxY21u0tL+K9ImQuN1t4GMd0hFb2NyTE2s1Ki2Sh9lHCFEwMl6MtiswOLt2mqLnqrQLJvBfIghRd+5WZc5Du9t8VDiRtHC4hjcHjnrz3shRkjj6NhFyURGyZ7uR/M/S0V3fnw5XLXCdELUv25+fs4jUI1NkidjJalOUdUMB1OijGfMjO0m0LH4HoOu+ZDAMgxjP+1KVCOVU2YhdI7gg4QknpRq3adaU4JE/VQd+QZBqShb6/t7An8JpzHo/9UY/8pBmkI2XrMAeW"
    }
}
xml_msg_6 = '''<?xml version="1.0" encoding="utf-8"?>
<message>
  <method>logIn</method>
  <parametrs>
    <name> Denis </name>
    <password>'''+base64.b64encode(ciphertext).decode()+'''</password>
  </parametrs>
</message>'''

xml_msg_6 = xml_msg_6.encode("utf-8")


msg8 = {
    "method": "getPublicKey"
}
xml_msg_8 = b'''<?xml version="1.0" encoding="utf-8"?>
<message>
  <method>getPublicKey</method>
</message>'''



msg7 = {
    "method" : "getLast",
    "parametrs": {
        "ObjectID": 1
    }
}

msg9 = {
    "method" : "getWarning",
    "parametrs": {
        "ObjectID": 1
    }
}
xml_msg_9 = b'''<?xml version="1.0" encoding="utf-8"?>
<message>
  <method>getWarning</method>
  <parametrs>
    <ObjectID type="int"> 1 </ObjectID>
  </parametrs>
</message>'''


xml_msg_7 = b'''<?xml version="1.0" encoding="utf-8"?>
<message>
  <method>getLast</method>
  <parametrs>
    <ObjectID type="int"> 1 </ObjectID>
  </parametrs>
</message>'''


def getLength(Socket):
    length = 0
    while not length:
        length = int(Socket.recv(1024).decode())
    Socket.sendall(bytes(length))
    return length

def setLength(Socket,msg):
    Socket.sendall(bytes(len(msg)))
    length = int(Socket.recv(1024).decode())
    while not len(msg) == length:
        length = int(Socket.recv(1024).decode())

    return length
msg = [
    # msg1,
    # ,msg2,msg3,msg4,msg5,
    # msg6,
    # msg7,
    # msg8
    # msg9
    xml_msg_6,
    xml_msg_7,
    xml_msg_8,
    xml_msg_9
]

# HOST, PORT = "25.79.246.93", 50000
# HOST, PORT = "192.168.1.100", 50000


def getLocalExternalIP():
    # getlockal ip
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temp_socket:
        temp_socket.connect(("8.8.8.8", 80))
        HOST = str(temp_socket.getsockname()[0])
        print("Lockal ip: {}".format(HOST))
    return HOST


# HOST, PORT = getLocalExternalIP(), 50000
HOST, PORT = "localhost", 9999
# Create a socket (SOCK_STREAM means a TCP socket)
for dataMsg in msg:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        data = dataMsg #str(dataMsg).encode('utf-8')
        sock.sendall(data)
        lenght = 10240
        received = sock.recv(lenght).decode('utf-8')
        print("Sent:     {}".format(data))
        print("Received: {}".format(received))
        print("------")