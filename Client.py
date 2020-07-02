import socket


msg1 = {
    "method": "get",
    "parametrs": {
        "collectionName": "radiator",
        "filter": {
            "Temperature": {'$gt': 90}
        }
    }
}

msg2 = {
    "method": "delete",
    "parametrs": {
        "collectionName": "radiator",
        "filter": {
            "Temperature": {'$lt': 0}
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


HOST, PORT = "localhost", 50000
data = str(msg1).encode()
# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
    # Connect to server and send data
    socket.connect((HOST, PORT))
    # socket.sendall(data)
    # Receive data from the server and shut down
    # length = int(sock.recv(1024).decode())
    # setLength(socket,data)
    socket.sendall(data)
    # lenght = getLength()
    lenght = 10240
    received = socket.recv(lenght).decode()

print("Sent:     {}".format(data))
print("Received: {}".format(received))






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
