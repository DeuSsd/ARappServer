import socketserver
import socket
from server import handlerJSON


def getLocalExternalIP():
    # getlockal ip
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temp_socket:
        temp_socket.connect(("8.8.8.8", 80))
        HOST = str(temp_socket.getsockname()[0])
        print("Lockal ip: {}".format(HOST))
    return HOST


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        lenght = 10240
        self.data = self.request.recv(lenght).decode()
        print("------------\n"
              "Client address: {}:{}\n"
              "Request: {}".format(*self.client_address, self.data))
        responseMsg = handlerJSON.loadMessage(self.data)
        print("Responce: {}".format(responseMsg))
        msg = str(responseMsg).encode()
        self.request.sendall(msg)

if __name__ == "__main__":
    HOST, PORT = getLocalExternalIP(), 50000
    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running
        server.serve_forever()
        server.server_close()
