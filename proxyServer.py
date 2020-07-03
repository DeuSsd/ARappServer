import socketserver
from server import handlerJSON

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        lenght = 10240
        self.data = self.request.recv(lenght).decode()

        print(self.data)
        responseMsg = self.data
        msg = str(responseMsg).encode()
        self.request.sendall(msg)
        print("------")

if __name__ == "__main__":
# HOST, PORT = "25.79.246.93", 50000
    HOST, PORT = "127.0.0.1", 50000
    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
        server.server_close()
