import socketserver
import socket
from server import handlerJSON


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # lenght = self.getLength(self.request)
        lenght = 10240
        self.data = self.request.recv(lenght).decode()  # .strip()
        print("------------\nClient address: {}:{}\nRequest: {}".format(*self.client_address, self.data))
        # print("{} wrote:".format(self.client_address[0]))
        # print(pickle.loads(self.data))
        # print(self.data)
        # socket.sendto(data, self.client_address)
        responseMsg = handlerJSON.loadMessage(self.data)
        print("Responce: {}".format(responseMsg))
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
    #getlockal ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    # print(s.getsockname()[0])
    HOST, PORT = "25.79.246.93", 9090
    # HOST, PORT = s.getsockname()[0], 50000
    s.close()
    print(HOST)
    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
        server.server_close()
