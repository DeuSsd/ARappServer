from ftplib import FTP
import socket
import re
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

def getLocalExternalIP():
    # getlockal ip
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temp_socket:
        temp_socket.connect(("8.8.8.8", 80))
        HOST = str(temp_socket.getsockname()[0])
        # print("Lockal ip: {}".format(HOST))
    return HOST


HOST = ''
LocalIP = getLocalExternalIP()
PORT_server = 15000
PORT_client = 12000
DIRECTORY_SCRIPTS = '/CS'


# checking the ip address format
def is_ok(text):
    match = re.match(
        """^(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{2}|[0-9])(\.(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{2}|[0-9])){3}$""",
        text)
    return bool(match)


def pause():
    programPause = input("\nPress the <ENTER> key to continue...")


def progressBar(iterable, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)

    # Progress Bar Printing Function
    def printProgressBar(iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\rDownloaded files: {iteration}/{total}: '
              f'{prefix} |{bar}| {percent}% {suffix}', end=printEnd)

    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()


# TODO
# Traceback (most recent call last):
#   File "C:/AR-Project/AR-Server/server/FTP_Proxy.py", line 210, in <module>
#     fileUpdate()
#   File "C:/AR-Project/AR-Server/server/FTP_Proxy.py", line 142, in fileUpdate
#     printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)
#   File "C:/AR-Project/AR-Server/server/FTP_Proxy.py", line 117, in printProgressBar
#     percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
# ZeroDivisionError: float division by zero

import time


def fileUpdate(dir):
    # print(dir)
    ftp = FTP('')
    ftp.connect(HOST, PORT_server)
    ftp.login()
    ftp.cwd(DIRECTORY_SCRIPTS)  # replace with your directory

    def downloadFile(filename):
        # filename = 'Client.cs' #replace with your file in the directory ('directory_name')
        # localfile = open('CS_test/' + filename, 'wb')
        localfile = open(dir + '/' + filename, 'wb')
        ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
        localfile.close()

    listOfScripts = ftp.nlst()

    for item in progressBar(listOfScripts, prefix='Progress:', suffix='Complete', length=40):
        # print(item)
        downloadFile(item)
        # time.sleep(0.1)
        # print(i)
        # printProgressBar(i+1, l, prefix='Progress:', suffix='Complete', length=50)

    ftp.quit()


def startFTP():
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    authorizer.add_user('user', '12345', '.', perm='elradfmwMT')
    authorizer.add_anonymous(os.getcwd())

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    # handler.masquerade_address = '151.25.42.11'
    # handler.passive_ports = range(60000, 65535)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = (getLocalExternalIP(), 12000)
    # address = ('25.79.246.93', 9090)
    # print(address)
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # start ftp server
    server.serve_forever()




def createDir():
    # определяем текущий каталог и печатаем
    dirName = "Prefubs"
    path = os.getcwd()
    try:
        if not os.path.isdir(dirName):
            os.mkdir(dirName)
        os.chdir(dirName)
        path = os.getcwd()
    except OSError:
        pass
    return path




if __name__ == "__main__":
    try:
        # with tempfile.TemporaryDirectory() as directory:
        # gethamachi ip
        try:
            f = open("hamachiIP.txt", "r")
        except:
            f = open("hamachiIP.txt", "w")
            raise TypeError
        HOST = f.read()
        f.close()
        if not is_ok(HOST):
            raise TypeError
        path = createDir()
        print("------ Loading the IP configuration ------\n"
              "FTP-Server ip:   {}\n"  # Hamachi IP
              "Lockal ip:       {}\n"
              "------------ Connection start ------------\n".format(HOST, LocalIP))
        print("-------- Start to update scripts ---------")
        fileUpdate(path)
        print("----- All scripts have been updated ------")
        print("------------ Start FTP-Server ------------")
        startFTP()
    except TypeError:
        print("\nДля запуска прокси-сервера выполните следующие действия:\n"
              "--> Узнайте IPv4 тонельного соединения в hamachi.\n"
              "--> Запишите его в hamachiIP.txt в виде \"xxx.xxx.xxx.xxx\" (без кавычек и других символов).\n"
              "--> И перезапустите \"ftpProxy\".")
    except OSError:
        print("\nДля запуска прокси-сервера выполните следующие действия:\n"
              "--> Убедитесь, что FTP Server запущен на хосте\n"
              "--> Убедитесь, что запущена одна версия программы\"ftpProxy\".\n"
              "--> Проверьте интернет соединение и перезапустите \"ftpProxy\".")
    f.close()
    pause()
