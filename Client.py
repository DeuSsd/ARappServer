import socket
import time

#
# def client(ip, port, message):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.connect((ip, port))
#     try:
#         while True:
#             time.sleep(5)
#             sock.sendall(message)
#             response = sock.recv(1024)
#             print(")Received: {}".format(response))
#     finally:
#         sock.close()
#
#
# if __name__ == '__main__':
#     client(*('127.0.0.1', 56075), "Hello World 1")

# # Import socket module
# import socket
#
#
# def Main():
#     # local host IP '127.0.0.1'
#     host = '127.0.0.1'
#
#     # Define the port on which you want to connect
#     port = 12345
#
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#     # connect to server on local computer
#     s.connect((host, port))
#
#     # message you send to server
#     message = "shaurya says geeksforgeeks"
#     while True:
#
#         # message sent to server
#         s.send(message.encode('ascii'))
#
#         # messaga received from server
#         data = s.recv(1024)
#
#         # print the received message
#         # here it would be a reverse of sent message
#         print('Received from the server :', str(data.decode('ascii')))
#
#         # ask the client whether he wants to continue
#         ans = input('\nDo you want to continue(y/n) :')
#         if ans == 'y':
#             continue
#         else:
#             break
#     # close the connection
#     s.close()
#
#
# if __name__ == '__main__':
#     Main()
#
# # import socket
# # import time
# #
# # msg1 = {
# #     "method": "get",
# #     "parametrs": {
# #         "collectionName": "radiator",
# #         "filter": {
# #             "Temperature": {'$gt': 95}
# #         }
# #     }
# # }
# #
# # msg2 = {
# #     "method": "delete",
# #     "parametrs": {
# #         "collectionName": "radiator",
# #         "filter": {
# #             "Temperature": {'$lt': 10}
# #         }
# #     }
# # }
# #
# # msg3 = {
# #     "method": "put",
# #     "parametrs": {
# #         "collectionName": "radiator",
# #         "data": {
# #             "Temperature": 150.256
# #         }
# #     }
# # }
# #
# # msg5 = {
# #     "method": "put"
# # }
# #
# # msg4 = {
# #     "method": "get",
# #     "parametrs": {
# #         "collectionName": "radiator",
# #         "filter": {
# #             "Temperature": {'$gt': 150}
# #         }
# #     }
# # }
# #
# #
# # def getLength(Socket):
# #     length = 0
# #     while not length:
# #         length = int(Socket.recv(1024).decode())
# #     Socket.sendall(bytes(length))
# #     return length
# #
# # def setLength(Socket,msg):
# #     Socket.sendall(bytes(len(msg)))
# #     length = int(Socket.recv(1024).decode())
# #     while not len(msg) == length:
# #         length = int(Socket.recv(1024).decode())
# #
# #     return length
# # msg = [msg1,msg2,msg3,msg4,msg5]
# # #getlockal ip
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("8.8.8.8", 80))
# print(s.getsockname()[0])
# HOST, PORT = "25.79.246.93", 9090
HOST, PORT = "localhost", 9999
# s.close()
# HOST, PORT = "25.79.246.93", 50000
# HOST, PORT = "localhost", 40000
# Create a socket (SOCK_STREAM means a TCP socket)
# for dataMsg in msg:
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        # while True:
        sock.connect((HOST, PORT))
        # socket.sendall(data)
        # Receive data from the server and shut down
        # length = int(sock.recv(1024).decode())
        # setLength(socket,data)

        dataMsg = "asda"
        # time.sleep(0.001)
        data = str(dataMsg).encode()
        sock.sendall(data)
        # lenght = getLength()
        lenght = 4096
        received = sock.recv(lenght)
        # print("Sent:     {}".format(data))
        # print("Received: {}".format(received))
        # print("------")
        time.sleep(0.1)
        sock.close()
# #
# #
# #
# #
# #
# #
# #
# #
# # # import multiprocessing
# # # import multiprocessing.connection as connection
# #
# # # def producer(data, address, authkey):
# # #     with connection.Listener(address, authkey=authkey) as listener:
# # #         with listener.accept() as conn:
# # #             print('connection accepted from', listener.last_accepted)
# # #             for item in data:
# # #                 print("producer sending:", repr(item))
# # #                 conn.send(item)
# # #
# # # def consumer(address, authkey):
# # #     with connection.Client(address, authkey=authkey) as conn:
# # #         try:
# # #             while True:
# # #                 item = conn.recv()
# # #                 print("consumer received:", repr(item))
# # #         except EOFError:
# # #             pass
# # #
# # # listen_address = "localhost", 50000
# # # remote_address = "localhost", 50000
# # # authkey = b'secret password'
# # #
# # # if __name__ == "__main__":
# # #     data = ["1", "23", "456"]
# # #     p = multiprocessing.Process(target=consumer, args=(data, listen_address, authkey))
# # #     p.start()
# # #     consumer(remote_address, authkey)
# # #     p.join()
# # #     print("done")
