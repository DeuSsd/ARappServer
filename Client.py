import socket
import rsa
import time

# для тестов
msg1 = {
    "method": "get",
    "parametrs": {
        "collectionName": "radiator",
        "filter": {
            "Temperature": {'$gt': 95}
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
        "name": "Vova",
        "password": b'\x15\xa2\x8a\xbb\xb5q\xb8w\x8fy\xe0\xb1\xb1\xb6\xc3\xf1\x9b\xb19\xa3\xac[\xcf\x15%\xaeh\x06\xa0\xde|\xfe\xa4xw\xe6\x94\xefE\x9b79&\xf7\x01\x1d\xb2"QVr\xa9\x97\x0b,L\x1e\xbb\xeb\x97\xf5\xa6J#\xff\x10m\xe78[q\xa2\xcac\xd0z\x04j\xc1\x1a\xdb2{\x92\x03n\xff\x1a\xac\x04\x9b\xad\xfa\xb6\xc8XtR}\x15?\x0e\xc4\xd1n\x90\xbbER\xd22&\xa0\x0b\x9d P\xdeG\xfc\x82ol\x88\x9d\xd0{\t*U\xc5\xb9g\x9d\xef3\xe8\x90\xa2r\xba\xb7\x8eqH\xb2C\x9e \xeb\xa0e\xd0\x17\xde$\xd0\x86m\xb6\xb8/+\x963g+\x10(zHqY\x1d\n\xf3U\xeb\xfc#\x0eu#L\xfdBu\x1d-\xf45\xb7\x03\x04\x95\xa4z\rY\xfeg\\kCa\xa8]\xd7\xd5T\xe2\xe0\x03>\xaa\xea\xf1~\xf7\x1e%@W\xdc)\x02\x96E\xa0\t\xb0\xef\xb0\x82]\xa7b\xe0\xfc\xb6\xba\xae|\xcd\xf6\t\xe6L\xf5\x8a\x9f\x85\xaa5\xfew'
    }
}


def getLocalExternalIP():
    # getlockal ip
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temp_socket:
        temp_socket.connect(("8.8.8.8", 80))
        HOST = str(temp_socket.getsockname()[0])
        print("Lockal ip: {}".format(HOST))
    return HOST


# msg = [msg1, msg2, msg3, msg4, msg5]
msg = [msg6]
HOST, PORT = getLocalExternalIP(), 50000
# Create a socket (SOCK_STREAM means a TCP socket)
for dataMsg in msg:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        data = str(dataMsg).encode('utf8')
        sock.sendall(data)
        lenght = 10240
        received = sock.recv(lenght).decode('utf8')
        print("Sent:     {}".format(data))
        print("Received: {}".format(received))
        print("------")
