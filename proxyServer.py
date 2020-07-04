import socketserver
import socket
import re

hamachiIP = ""
hamachiPORT = 9090

# проверка ip на корректность
def is_ok(text):
    match = re.match(
        """^(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{2}|[0-9])(\.(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{2}|[0-9])){3}$""",
        text)
    return bool(match)


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        lenght = 10240
        self.data = self.request.recv(lenght)
        print(self.data)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((hamachiIP, hamachiPORT))
            sock.sendall(self.data)
            print("-----*****\nData from client to server: {} ".format(self.data))
            lenght = 10240
            received = sock.recv(lenght)
        self.request.sendall(received)
        print("Data from server to client: {} \n *****-----".format(received))

if __name__ == "__main__":
    try:
        # gethamachi ip
        try:
            f = open("hamachiIP.txt", "r")
        except:
            f = open("hamachiIP.txt", "w")
            raise TypeError
        hamachiIP = f.read()
        if not is_ok(hamachiIP):
            raise TypeError

        # getlockal ip
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        HOST, PORT = s.getsockname()[0], 50000
        s.close()
        print("------ Load ip in programm ------\n"
              "Server ip: {}\n" #Hamachi IP
              "Lockal ip: {}\n"
              "------- Connection start --------".format(hamachiIP, HOST))

        # Create the server, binding to localhost on port 9999
        with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            server.serve_forever()
            server.server_close()
    except TypeError:
        print("Узнайте IPv4 тонельного соединения в hamachi;\n"
              "Запишите его в hamachiIP.txt в виде \"xxx.xxx.xxx.xxx\" (без кавычек и других символов)\n"
              "И перезапустите proxyServer")
    except OSError:
        print("Проверьте интернет соединение и перезапустите proxyServer")
