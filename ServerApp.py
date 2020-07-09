import socketserver
import socket
import threading
from server import handlerJSON


class ThreadedRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        length = 1024
        data = self.request.recv(length)
        current_thread = threading.current_thread()
        response = b'%s:%s' % (current_thread.getName().encode(), data)
        self.request.send(response)


# class ThreadedServer(socketserver.Threa)


if __name__ == "__main__":
    HOST,PORT = "localhost",0
    server = socketserver.ThreadingTCPServer((HOST,PORT),ThreadedRequestHandler)

    ip,port = server.server_address
    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)
    t.start()
    print('Server loop running is thread:',t.getName())

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((ip,port))

         # Send the data
        message = b'Hello, world'
        print('Sending : {!r}'.format(message))
        len_sent = s.send(message)

        # Receive a response
        response = s.recv(1024)
        print('Received: {!r}'.format(response))

















# class TCPHandler(socketserver.BaseRequestHandler):
#
#     def handle(self):
#
#         print("Hi")
#
#
# class ThreadingUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
#     pass
#


# if __name__ == "__main__":
#
#     HOST,PORT = "localhost",40000
#     print(HOST)
#     with socketserver.ThreadingTCPServer((HOST,PORT),TCPHandler) as server:
#         server.serve_forever()
#         server_threading = threading.Thread(target=server.serve_forever)

# class MyTCPHandler(socketserver.StreamRequestHandler):
# def handle(self):

# # lenght = self.getLength(self.request)
# lenght = 10240
# self.data = self.request.recv(lenght).decode()  # .strip()
# print("------------\nClient address: {}:{}\n"
#       "Request: {}".format(*self.client_address, self.data))
# # print("{} wrote:".format(self.client_address[0]))
# # print(pickle.loads(self.data))
# # print(self.data)
# # socket.sendto(data, self.client_address)
# responseMsg = handlerJSON.loadMessage(self.data)
# print("Responce: {}".format(responseMsg))
# msg = str(responseMsg).encode()
# # self.setLength(self.request,msg)
# self.request.sendall(msg)
# print("Hi")

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

# class ThreadingUDPServer(ThreadingMixIn, UDPServer):
#     pass

# if __name__ == "__main__":
# getlockal ip
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("8.8.8.8", 80))
# print(s.getsockname()[0])
# HOST, PORT = "25.79.246.93", 9090
# HOST, PORT = s.getsockname()[0], 40000
# s.close()
# print(HOST)
# Create the server, binding to localhost on port 9999
# with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
# server.serve_forever()
# server.server_close()


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


# class MyTCPHandler(socketserver.BaseRequestHandler):
#     """
#     The request handler class for our server.
#
#     It is instantiated once per connection to the server, and must
#     override the handle() method to implement communication to the
#     client.
#     """
#
#     def handle(self):
#         # self.request is the TCP socket connected to the client
#         self.data = self.request.recv(1024).strip()
#         print("{} wrote:".format(self.client_address[0]))
#         print(self.data)
#         # just send back the same data, but upper-cased
#         self.request.sendall(self.data.upper())
#
#
# if __name__ == "__main__":
#     HOST, PORT = "localhost", 9999
#
#     # Create the server, binding to localhost on port 9999
#     with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
#         # Activate the server; this will keep running until you
#         # interrupt the program with Ctrl-C
#         server.serve_forever()
