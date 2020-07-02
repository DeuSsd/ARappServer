import socket

Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Socket.bind(('127.0.0.1', 8888))
# Socket.accept()
msg = Socket.recv(1024)
print(msg)
Socket.close()
