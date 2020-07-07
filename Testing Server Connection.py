import socket
import datetime
import re
import ast

#checking the ip address format
def is_ok(text):
    match = re.match(
        """^(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{2}|[0-9])(\.(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{2}|[0-9])){3}$""",
        text)
    return bool(match)

def pause():
    programPause = input("\n--> При необходимости измените текст запроса в файле JSON_REQUEST.txt.\n"
                         "--> Сохраните файл JSON_REQUEST.txt.\n"
                         "--> Нажмите Enter для повторной отпраки запроса.\n")


def load():
    try:
        f = open("JSON_REQUEST.txt", "r")
    except:
        f = open("JSON_REQUEST.txt", "w")
    # JSON_REQUEST = f.read().replace("\n","")
    JSON_REQUEST = f.read().replace(" ","").replace("\n","")
    # print(ast.literal_eval(JSON_REQUEST))
    # print(JSON_REQUEST)
    f.close()
    return JSON_REQUEST


if __name__ == "__main__":
    # Create a socket (SOCK_STREAM means a TCP socket)
    # getlockal ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    HOST, PORT = s.getsockname()[0], 50000
    s.close()
    print("------ Loading the IP configuration ------\n"
          "Lockal (Server) ip: {}\n"
          "------------ Connection start ------------".format(HOST))
    while True:
        dataMsg = load()
        # Create the server, binding to localhost on port 9999
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            data = str(dataMsg).encode()
            print("----------- Start transmission -----------")
            sock.sendall(data)
            print("[----- C -> S -----] {}\n"
                  "Data transmission from client to server: \n{}".format(
                datetime.datetime.now().isoformat("|", "microseconds"), data.decode()))
            lenght = 10240
            received = sock.recv(lenght).decode()
            print("[----- C <- S -----] {}\n"
                  "Data transmission from server to client: \n{}\n"
                  "---------- End of transmission -----------".format(
                datetime.datetime.now().isoformat("|", "microseconds"), received))
        pause()