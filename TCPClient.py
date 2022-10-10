'''
@File    :   TCPClient.py
@Time    :   2022/10/10 19:50:23
@Author  :   Zhang Maysion 
@Version :   1.0
@Contact :   zhangmx67@mail2.sysu.edu.cn
'''



'''
from socket import *
serverName = 'LAPTOP-MAYSION'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
sentence = raw_input('Input lowercase sentence:')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('From Server: ', modifiedSentence.decode())
clientSocket.close()
'''


import socket
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 12000
ADDR = (IP, PORT)
FORMAT = 'utf-8'
SIZE = 1024
PATH = "CLIENT"


def list():
    pass

def download():
    pass

def upload():
    pass




def main():
    print(f"[INITIALIZING] Check whether the directory {PATH} exists")
    if not os.path.exists(PATH):
        print(f"[CHECK] The directory {PATH} does not exist")
        os.makedirs(PATH)
        print(f"[MAKEDIR] the directory {PATH} created")
    else:
        print(f"[CHECK] The directory {PATH} exists")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ADDR))

    file = open(PATH + "\\" + "test.txt", 'r')
    data = file.read()
  
    client.send("test.txt".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    client.send(data.encode())
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")



if __name__ == '__main__':
    main()