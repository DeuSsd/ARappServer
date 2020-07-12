# import socketserver
# import socket
# import handlerJSON
# import asynio
#
# class MyTCPHandler(socketserver.BaseRequestHandler):
#
#     def handle(self):
#         # lenght = self.getLength(self.request)
#         lenght = 10240
#         self.data = self.request.recv(lenght).decode()  # .strip()
#         print("------------\nClient address: {}:{}\nRequest: {}".format(*self.client_address, self.data))
#         # print("{} wrote:".format(self.client_address[0]))
#         # print(pickle.loads(self.data))
#         # print(self.data)
#         # socket.sendto(data, self.client_address)
#         responseMsg = handlerJSON.loadMessage(self.data)
#         print("Responce: {}".format(responseMsg))
#         msg = str(responseMsg).encode()
#         # self.setLength(self.request,msg)
#         self.request.sendall(msg)
#
#     # def getLength(self,Socket):
#     #     length = 0
#     #     while not length:
#     #         length = int(Socket.recv(1024).decode())
#     #     Socket.sendall(bytes(length))
#     #     return length
#     #
#     # def setLength(self,Socket, msg):
#     #     Socket.sendall(len(msg))
#     #     length = int(Socket.recv(1024).decode())
#     #     if len(msg) == length:
#     #         return length
#
#
#
# if __name__ == "__main__":
#     #getlockal ip
#     HOST, PORT = 'localhost', 9999
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.connect(("8.8.8.8", 80))
#     # print(s.getsockname()[0])
#     # HOST, PORT = "25.79.246.93", 9090
#     # HOST, PORT = s.getsockname()[0], 50000
#     s.close()
#     print(HOST)
#     # Create the server, binding to localhost on port 9999
#     with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
#         # Activate the server; this will keep running until you
#         # interrupt the program with Ctrl-C
#         server.serve_forever()
#         server.server_close()
#




import socket
from select import select
from server import handlerJSON

HOST, PORT = 'localhost', 9999

tasks = [] #тут используется модуль

to_read = {}
to_write = {}


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    while True:
        yield ('read', server_socket)
        client_socket, addr = server_socket.accept()
        print('Connection from ', addr)
        tasks.append(client(client_socket))

def client(client_socket):
    while True:
        yield ('read', client_socket)
        request = client_socket.recv(4096)

        # print(request)
        if not request:
            break
        else:
            response = handlerJSON.loadMessage(request.decode())
            msg =str(response).encode()
            yield ('write',client_socket)
            client_socket.send(msg)
    client_socket.close()


def event_loop():
    while any([tasks,to_read,to_write]):
        while not tasks:
            print(len(tasks),len(to_read),len(to_write))
            ready_to_read,ready_to_write,_= select(to_read,to_write,[])
            # print(ready_to_read,ready_to_write)
            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))
                # print(tasks)

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            task = tasks.pop(0)
            reason,sock = next(task)
            if reason == 'read':
                to_read[sock] = task
            if reason == 'write':
                to_write[sock] = task
        except StopIteration:
            # print("I'm died again!")
            pass


if __name__ == '__main__':
   tasks.append(server())
   event_loop()

