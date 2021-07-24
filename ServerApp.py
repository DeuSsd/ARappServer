import socket
from select import select
from ARappServer import HandlerRequest
from ARappServer.Authentification import checkRSA_PrivateKey, WrongRSA_Key
from ARappServer.encryptionDES import WrongDES_Key, checkDES_Key
import datetime

HOST, PORT = 'localhost', 50000
# HOST, PORT = '25.36.227.49', 9090
#HOST, PORT = '25.47.76.161', 9090
# HOST, PORT = "192.168.43.2", 50000

tasks = []  # тут должен использоваться модуль

to_read = {}
to_write = {}


# просто пауза
def pause():
    input("\nPress the <ENTER> key to continue...")


def server():
    '''
    Серверный модуль, отвечающий за установление соединения с клиентами
    ассинхронный
    :return: None
    '''
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
    '''
    Клиентский модуль, отвечающий за передачу данных от(к) клиента(у)
    ассинхронный
    :param client_socket: <class 'socket.socket'> принимает объект сокета,
            через который клиент общается с сервером
    :return: None
    '''
    while True:
        yield ('read', client_socket)
        request = client_socket.recv(4096)
        # print(request)
        if not request:
            break
        else:
            print("--------- Start of transmission ----------"
                  f"------------\nClient address: {client_socket.getpeername()[0]}:"
                  f"{client_socket.getpeername()[1]}\n"
                  f"[----- S <- C -----] {datetime.datetime.now().isoformat('|', 'microseconds')}\n"
                  f"Data transmission from client to server: \n\t{request.decode()}")

            response = HandlerRequest.loadMessage(request.decode())  # block process
            # msg = str(response).encode()
            msg = response
            yield ('write', client_socket)
            # print("Responce: {}".format())
            client_socket.send(msg)
            print(f"[----- S -> C -----] {datetime.datetime.now().isoformat('|', 'microseconds')}\n"
                  f"Data transmission from client to server: \n\t{msg.decode()}\n"
                  "---------- End of transmission -----------\n")
    client_socket.close()


def event_loop():
    while any([tasks, to_read, to_write]):

        while not tasks:
            # print(f'Количество клиентов: {len(to_read) + len(to_write) - 1}')
            print(f"t|r|w -- {len(tasks)}|{len(to_read)}|{len(to_write)}")  # показывает колличество клиентов
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])
            # print(ready_to_read,ready_to_write)
            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))
                # print(tasks)
            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            task = tasks.pop(0)
            reason, sock = next(task)
            if reason == 'read':
                to_read[sock] = task
            if reason == 'write':
                to_write[sock] = task
        except StopIteration:
            # print("I'm died again!")
            pass


if __name__ == '__main__':
    try:
        print("------ Loading the IP configuration ------\n"
              f"Server ip: {HOST}\n"  # Hamachi IP
              # "Lockal ip: {}\n"
              "------------ Connection start ------------")
        # print(HOST)
        checkDES_Key()
        checkRSA_PrivateKey()  # проверка на наличие ключей
        tasks.append(server())
        event_loop()
    except WrongDES_Key as exDES:
        print(exDES.message)
        pause()
    except WrongRSA_Key as exRSA:
        print(exRSA.message)
        pause()
