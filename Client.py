# import socket
# import datetime
# import jsonrpc
#
# dataj = [
#     {
#         "Temperature": 74.74,
#         "DateTime": datetime.datetime(2020, 6, 30, 21, 14, 53)
#     },
#     {
#         "Temperature": 34.77,
#         "DateTime": datetime.datetime(2020, 6, 30, 21, 15, 22)
#     },
#     {
#         "Temperature": 57.23,
#         "DateTime": datetime.datetime(2020, 6, 30, 21, 16, 45)
#     },
#     {
#         "Temperature": 20.22,
#         "DateTime": datetime.datetime(2020, 6, 30, 21, 17, 25)
#     },
# ]
# for data in dataj:
#     data["DateTime"] = str(data["DateTime"])
#
# HOST, PORT = "localhost", 9901
# data = str(dataj).encode()
# # Create a socket (SOCK_STREAM means a TCP socket)
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#     # Connect to server and send data
#     sock.connect((HOST, PORT))
#     sock.sendall(data)
#     # Receive data from the server and shut down
#     received = sock.recv(1024).decode()
#
# print("Sent:     {}".format(data))
# print("Received: {}".format(received))
#

import multiprocessing
import multiprocessing.connection as connection

def producer(data, address, authkey):
    with connection.Listener(address, authkey=authkey) as listener:
        with listener.accept() as conn:
            print('connection accepted from', listener.last_accepted)
            for item in data:
                print("producer sending:", repr(item))
                conn.send(item)

def consumer(address, authkey):
    with connection.Client(address, authkey=authkey) as conn:
        try:
            while True:
                item = conn.recv()
                print("consumer received:", repr(item))
        except EOFError:
            pass

listen_address = "localhost", 50000
remote_address = "localhost", 50000
authkey = b'secret password'

if __name__ == "__main__":
    data = ["1", "23", "456"]
    p = multiprocessing.Process(target=consumer, args=(data, listen_address, authkey))
    p.start()
    consumer(remote_address, authkey)
    p.join()
    print("done")
