from ftplib import FTP
import socket
def getLocalExternalIP():
    # getlockal ip
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temp_socket:
        temp_socket.connect(("8.8.8.8", 80))
        HOST = str(temp_socket.getsockname()[0])
        print("Lockal ip: {}".format(HOST))
    return HOST

ftp = FTP('')
# ftp.connect('localhost',1026)
ftp.connect(getLocalExternalIP(),1026)
ftp.login()
ftp.cwd('') #replace with your directory
# ftp.retrlines('LIST')

# def uploadFile():
#  filename = 'testfile.txt' #replace with your file in your home folder
#  ftp.storbinary('STOR '+filename, open(filename, 'rb'))
#  ftp.quit()

def downloadFile():
 filename = 'Client.cs' #replace with your file in the directory ('directory_name')
 localfile = open(filename, 'wb')
 ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
 ftp.quit()
 localfile.close()

# uploadFile()
downloadFile()




