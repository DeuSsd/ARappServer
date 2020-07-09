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
#getlockal ip
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
# print(s.getsockname()[0])
# HOST, PORT = "25.79.246.93", 9090
HOST, PORT = s.getsockname()[0], 40000
s.close()
# HOST, PORT = "25.79.246.93", 50000
# HOST, PORT = "localhost", 40000
# Create a socket (SOCK_STREAM means a TCP socket)
for dataMsg in msg:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        # socket.sendall(data)
        # Receive data from the server and shut down
        # length = int(sock.recv(1024).decode())
        # setLength(socket,data)
        while True:
            dataMsg = 2
            time.sleep(1)
            data = str(dataMsg).encode()
            sock.sendall(data)
            # lenght = getLength()
            # lenght = 10240
            # received = sock.recv(lenght).decode()
            # time.sleep(1)
            print("Sent:     {}".format(data))
            # print("Received: {}".format(received))
            # print("------")








# import multiprocessing
# import multiprocessing.connection as connection

# def producer(data, address, authkey):
#     with connection.Listener(address, authkey=authkey) as listener:
#         with listener.accept() as conn:
#             print('connection accepted from', listener.last_accepted)
#             for item in data:
#                 print("producer sending:", repr(item))
#                 conn.send(item)
#
# def consumer(address, authkey):
#     with connection.Client(address, authkey=authkey) as conn:
#         try:
#             while True:
#                 item = conn.recv()
#                 print("consumer received:", repr(item))
#         except EOFError:
#             pass
#
# listen_address = "localhost", 50000
# remote_address = "localhost", 50000
# authkey = b'secret password'
#
# if __name__ == "__main__":
#     data = ["1", "23", "456"]
#     p = multiprocessing.Process(target=consumer, args=(data, listen_address, authkey))
#     p.start()
#     consumer(remote_address, authkey)
#     p.join()
#     print("done")
