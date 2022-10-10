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


def main():
    # initialize
    print(f"[INITIALIZING] Check whether the directory {PATH} exists")
    if not os.path.exists(PATH):
        print(f"[CHECK] The directory {PATH} does not exist")
        os.makedirs(PATH)
        print(f"[MAKEDIR] the directory {PATH} created")
    else:
        print(f"[CHECK] The directory {PATH} exists")
    
    print(f"[CONNECT] Ask a tcp connection")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ADDR))
    msg = client.recv(SIZE).decode(FORMAT)
    if msg == "Connect sucessfully":
        print("[STATUS] Connect to server successfully.")
    else:
        print("[STATUS] fail to connect to server.")
        return

    # we use number to tell server the task type
    # 0 : list the file name
    # 1 : download from server
    # 2 : upload to server
     
    def list():
        client.send("0".encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(msg)

    def download(filename):
        client.send("1".encode(FORMAT))
        file = open(PATH + "\\" + filename, 'w') 
        client.send(filename.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER]: {msg}")
        msg = client.recv(SIZE).decode(FORMAT)
        file.write(msg)
        file.close()
        print(f"[STATUS] Successfully download the file: {filename}")

    def upload(filename):
        client.send("2".encode(FORMAT))
        file = open(PATH + "\\" + filename, 'r')
        data = file.read()
    
        client.send(filename.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER]: {msg}")

        client.send(data.encode())
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER]: {msg}")
        print(f"[STATUS] Successfully update the file: {filename}")

    def build():
        filename = input("[BUILD] input the new file name:\n")
        file = open(filename, 'w')
        print("[HELP] to mark the end of file, input ':q' ")
        data = input("[BUILD] input a row of data for this new file:\n")
        while not data == ":q":
            file.write(data + '\n')
            print("[STATUS] Successfully write a data into the file")
            data = input("[BUILD] input a row of data for this new file:\n")
        file.close()
        print(f"[STATUS] Successfully build the file: {filename}")
            

    def help():
        print("[HELP] you can input command like:") 
        print("[HELP] - help") # ask for help about the command 
        print("[HELP] - list") # list the file name (also directory name in server dir)
        print("[HELP] - build") # build a new file (so that you can upload it to server)
        print("[HELP] - download filename") # download a file from server
        print("[HELP] - upload filename") # upload a file to server
        print("[HELP] - exit") # exit the client
    
    

    while True:
        command = input('[INPUT] input your command:\n')
        while len(command) < 4:
            print('[ERROR] Invalid command')
            print("[HELP] you can input 'help' to get help.")
            command = input('[INPUT] input your command:\n')
        if command.startswith('help'):
            help()
        elif command.startswith('list'):
            list()
        elif command.startswith('build'):
            build()
        elif command.startswith('download'):
            if len(command) < 10:
                print('[ERROR] Invalid command')
                print("[HELP] you can input command like:") 
                print("[HELP] - dwld filename")
                continue
            else:
                download(command[9:])
        elif command.startswith('upload'):
            if len(command) < 8:
                print('[ERROR] Invalid command')
                print("[HELP] you can input command like:") 
                print("[HELP] - upld filename")
                continue
            else:
                download(command[7:])
        elif command.startswith('exit'):
            break
        else:
            print('[ERROR] Invalid command')
            print("[HELP] you can input 'help' to get help.")
            continue

if __name__ == '__main__':
    main()