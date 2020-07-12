import socket
import time

msg1 = {
    "method": "get",
    "parametrs": {
        "collectionName": "radiator",
        "filter": {
            "Temperature": {'$lt': 50}
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


msg = [msg1,msg2,msg3]#,msg4#,msg5]
#getlockal ip
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("8.8.8.8", 80))
# print(s.getsockname()[0])
# HOST, PORT = "25.79.246.93", 9090
HOST, PORT = "localhost", 9999
# s.close()
# HOST, PORT = "25.79.246.93", 50000
# HOST, PORT = "localhost", 40000
# Create a socket (SOCK_STREAM means a TCP socket)
# msg = ["sd"]
while True:
    for dataMsg in msg:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            # while True:
            sock.connect((HOST, PORT))
            # socket.sendall(data)
            # Receive data from the server and shut down
            data = str(dataMsg).encode()
            sock.sendall(data)
            lenght = 20480
            received = sock.recv(lenght)
            # print("Sent:     {}".format(data))
            # print("Received: {}".format(received))
            # print("------")
            time.sleep(0.01)
            sock.close()
