import socketserver
import socket
import re

hamachiIP = ""
hamachiPORT = 9090

#checking the ip address format
def is_ok(text):
    match = re.match(
        """^(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{2}|[0-9])(\.(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{2}|[0-9])){3}$""",
        text)
    return bool(match)

def pause():
    programPause = input("\nPress the <ENTER> key to continue...")


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print("--------- Start of transmission ----------")
        lenght = 10240
        self.data = self.request.recv(lenght)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((hamachiIP, hamachiPORT))
            sock.sendall(self.data)
            print("[----- C -> S -----] "
                  "Data transmission from client to server:\n{}".format(self.data))
            lenght = 10240
            received = sock.recv(lenght)
        self.request.sendall(received)
        print("[----- C <- S -----] "
              "Data transmission from server to client:\n"
              "---------- End of transmission -----------\n".format(received))
if __name__ == "__main__":
    try:
        # gethamachi ip
        try:
            f = open("hamachiIP.txt", "r")
        except:
            f = open("hamachiIP.txt", "w")
            raise TypeError
        hamachiIP = f.read()
        f.close()
        if not is_ok(hamachiIP):
            raise TypeError

        # getlockal ip
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        HOST, PORT = s.getsockname()[0], 50000
        s.close()
        print("------ Loading the IP configuration ------\n"
              "\033[33mServer ip: {}\033[0m\n"  # Hamachi IP
              "\033[33mLockal ip: {}\033[0m\n"
              "------------ Connection start ------------\033[0m\n".format(hamachiIP, HOST))

        # Create the server, binding to localhost on port 9999
        with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
            # Activate the server; this will keep running
            server.serve_forever()
            server.server_close()
    except TypeError:
        print("Узнайте IPv4 тонельного соединения в hamachi;\n"
              "Запишите его в hamachiIP.txt в виде \"xxx.xxx.xxx.xxx\" (без кавычек и других символов)\n"
              "И перезапустите \"ProxyServer.exe\".\n")
    except OSError:
        print("Убедитесь, что запущена одна версия программы\"ProxyServer.exe\".\n"
              "Проверьте интернет соединение и перезапустите \"ProxyServer.exe\".\n")
    f.close()
    pause()