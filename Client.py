import socket
import time

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
msg = [msg1,msg2,msg3,msg4,msg5]

HOST, PORT = "25.79.246.93", 50000
# HOST, PORT = "192.168.1.105", 50000

# Create a socket (SOCK_STREAM means a TCP socket)
for dataMsg in msg:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        # socket.sendall(data)
        # Receive data from the server and shut down
        # length = int(sock.recv(1024).decode())
        # setLength(socket,data)
        data = str(dataMsg).encode()
        sock.sendall(data)
        # lenght = getLength()
        lenght = 10240
        received = sock.recv(lenght).decode()
        # time.sleep(1)
        print("Sent:     {}".format(data))
        print("Received: {}".format(received))
        print("------")

