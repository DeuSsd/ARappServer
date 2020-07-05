import socket
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

def getLocalExternalIP():
    # getlockal ip
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temp_socket:
        temp_socket.connect(("8.8.8.8", 80))
        HOST = str(temp_socket.getsockname()[0])
        print("Lockal ip: {}".format(HOST))
    return HOST

msg = [msg1, msg2, msg3, msg4, msg5]
HOST, PORT = getLocalExternalIP(), 50000
# Create a socket (SOCK_STREAM means a TCP socket)
for dataMsg in msg:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        data = str(dataMsg).encode()
        sock.sendall(data)
        lenght = 10240
        received = sock.recv(lenght).decode()
        print("Sent:     {}".format(data))
        print("Received: {}".format(received))
        print("------")

