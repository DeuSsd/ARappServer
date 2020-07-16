
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

msg6 = {
    "method": "logIn",
    "parametrs": {
        "collectionName": "users",
        "name": "Denis",
        "password": b"#6\x94l^\xaa\xa4w\x99\xc9/wM\x94\xd1C\x9f\xd5B\x10\xd8\xcf\x9fx1Z>\xa2\x8c\xba\x18N`\x80\xdc|\x05\xd4\xed\xb7\xb9U\x97\xa1=\t\x87\xf7t2\xe4\xf2\xe2\xe3\xdf}\xe62\x87\x9d\x99\x7fI\xee\xf2\xa6\xf0\t\xd6\x07\xc9J\xac\xb7\xd2/\xd6\xb5=\x97\xe4EX\xc0U.O\xef\xb8\x19\xcc\xe93p\xc2h\x84]\x06f\x87\xdd_\xe4\x16\xb7\xd3\xb08\xb6\xae\xfc\xcf\xc8\x0cfo\xb2\xff\x11_Q\xf6\x9d\xfa\x9b\x13\xd36d\x92&\x03\x16 \x83:\xbe)v\xce\xbb\xc5\xf9\xef\x80\xe3\xf6\xf1\xb9]\xf8H\xdb`\xbb5\xb3\x13*A\x0e5\x9a@\xf54!\x17\xc7\xbb5\xfc\xae\x03q\x8b`\x80*\xaa\xbb3\xf0\x82\xe0q\xa7\xf4P\xf2\xde-\x02S\x10S\x8b-\xf4\xdc}\xba\xb7\xe9lO}\xea\xe57C'\xa0\xf2S8\x04\x1f\xd4;+j\x8b\xde\xe3\x0c\xde\xf89|\xb0\x91\xdb\xf0X\xf2\xa4u&\xc1.c^I\xb36R@b\xad\xc0\xbf\xa3\xc2\xaa"
    }
}



msg7 = {
    "method" : "getLastData",
    "ObjectID": 1
}

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
    msg1,
    # ,msg2,msg3,msg4,msg5,
    msg6
    # msg7
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


# HOST, PORT = getLocalExternalIP(), 9999
HOST, PORT = "localhost", 9999
# Create a socket (SOCK_STREAM means a TCP socket)
for dataMsg in msg:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        data = str(dataMsg).encode('utf-8')
        sock.sendall(data)
        lenght = 10240
        received = sock.recv(lenght).decode('utf-8')
        print("Sent:     {}".format(data))
        print("Received: {}".format(received))
        print("------")
