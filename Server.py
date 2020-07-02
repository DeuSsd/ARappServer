import socket

Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Socket.bind(('127.0.0.1', 9901))
# Socket.accept()

length = int(Socket.recv(1024).decode())
msg = Socket.recv(length)
print(msg)
Socket.close()


def getLength(Socket,msg):
    length = 0
    while not length:
        length = int(Socket.recv(1024).decode())
    Socket.sendall(bytes(length))
    return length

def setLength(Socket, msg):
    Socket.sendall(len(msg))
    length = int(Socket.recv(1024).decode())
    if len(msg) == length:
        return length
    # else
    #     return 0
