import socket
from select import select
from server import handlerJSON


HOST, PORT = 'localhost', 9999
# HOST, PORT = "25.79.246.93", 9090

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
        # print('Connection from ', addr)
        tasks.append(client(client_socket))


def client(client_socket):
    while True:
        yield ('read', client_socket)
        request = client_socket.recv(4096)
        # print(request)
        if not request:
            break
        else:
            print("------------\nClient address: {}:{}\nRequest: {}".format(*client_socket.getpeername(), request.decode()))
            response = handlerJSON.loadMessage(request.decode()) #block process
            msg =str(response).encode()
            yield ('write',client_socket)
            print("Responce: {}".format(msg.decode()))
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
    print(HOST)
    tasks.append(server())
    event_loop()

# =======
# import socketserver
# import socket
# from server import handlerJSON
#
#
# def getLocalExternalIP():
#     # getlockal ip
#     with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temp_socket:
#         temp_socket.connect(("8.8.8.8", 80))
#         HOST = str(temp_socket.getsockname()[0])
#         print("Lockal ip: {}".format(HOST))
#     return HOST
#
#
# class MyTCPHandler(socketserver.BaseRequestHandler):
#
#     def handle(self):
#         lenght = 10240
#         self.data = self.request.recv(lenght).decode('utf8')
#         print("------------\n"
#               "Client address: {}:{}\n"
#               "Request: {}".format(*self.client_address, self.data))
#         responseMsg = handlerJSON.loadMessage(self.data)
#         print("Responce: {}".format(responseMsg))
#         msg = str(responseMsg).encode('utf8')
#         self.request.sendall(msg)
#
# if __name__ == "__main__":
#     HOST, PORT = getLocalExternalIP(), 50000
#     # Create the server, binding to localhost on port 9999
#     with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
#         # Activate the server; this will keep running
#         server.serve_forever()
#         server.server_close()
# >>>>>>> dev
