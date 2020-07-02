import socketserver
from server import handlerJSON
# import pickle

    # else
    #     return 0


class MyTCPHandler(socketserver.BaseRequestHandler):



    def handle(self):
        # lenght = self.getLength(self.request)
        lenght = 10240
        self.data = self.request.recv(lenght).decode()  # .strip()

        # print("Address: {}".format(self.client_address[0]))
        # print("{} wrote:".format(self.client_address[0]))
        # print(pickle.loads(self.data))
        print(self.data)
        # socket.sendto(data, self.client_address)
        responseMsg = handlerJSON.loadMessage(self.data)
        msg = str(responseMsg).encode()
        # self.setLength(self.request,msg)
        self.request.sendall(msg)

    # def getLength(self,Socket):
    #     length = 0
    #     while not length:
    #         length = int(Socket.recv(1024).decode())
    #     Socket.sendall(bytes(length))
    #     return length
    #
    # def setLength(self,Socket, msg):
    #     Socket.sendall(len(msg))
    #     length = int(Socket.recv(1024).decode())
    #     if len(msg) == length:
    #         return length

if __name__ == "__main__":
    HOST, PORT = "localhost", 50000
    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
        server.server_close()

# import multiprocessing
# import multiprocessing.connection as connection

# def producer(data, address, authkey):
#     with connection.Listener(address, authkey=authkey) as listener:
#         with listener.accept() as conn:
#             print('connection accepted from', listener.last_accepted)
#             for item in data:
#                 print("producer sending:", repr(item))
#                 conn.send(item)

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
#     p = multiprocessing.Process(target=consumer, args=(remote_address, authkey))
#     p.start()
#     # consumer(remote_address, authkey)
#     p.join()
#     print("done")