import socketserver
import socket
HOST, PORT = "25.79.246.93", 9090

# def getLocalExternalIP():
#     # getlockal ip
#     with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temp_socket:
#         temp_socket.connect(("8.8.8.8", 80))
#         HOST = str(temp_socket.getsockname()[0])
#         print(HOST)
#     return HOST

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        lenght = 10240
        self.data = self.request.recv(lenght)  # .strip()
        print("------------\n"
              "Client address: {}:{}\n"
              "Request: {}".format(*self.client_address, self.data.decode()))
        responseMsg = self.data
        self.request.sendall(responseMsg)
        print("Responce: {}".format(responseMsg.decode()))

if __name__ == "__main__":
    # HOST, PORT = getLocalExternalIP(), 50000
    # Create the server, binding to localhost on port 50000
    print()
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
        server.server_close()



