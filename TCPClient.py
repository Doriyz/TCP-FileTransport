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


from dataclasses import field
from pydoc import cli
import socket
import os

# IP = socket.gethostbyname(socket.gethostname())
IP = 'LAPTOP-MAYSION'
# IP = 'Gulfira'
PORT = 12000
ADDR = (IP, PORT)
FORMAT = 'utf-8'
SIZE = 1024 
PATH = "CLIENT" 


def main():
    # initialize:check the directory to store files
    print(f"[INITIALIZING] Check whether the directory {PATH} exists")
    if not os.path.exists(PATH):
        print(f"[CHECK] The directory {PATH} does not exist")
        os.makedirs(PATH)
        print(f"[MAKEDIR] the directory {PATH} created")
    else:
        print(f"[CHECK] The directory {PATH} exists")
    
    # connect to server
    print(f"[CONNECT] Ask a tcp connection")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ADDR))
    msg = client.recv(SIZE).decode(FORMAT)
    print(msg)
 
    def list():
        client.send("list".encode(FORMAT))
        namestr = client.recv(SIZE).decode(FORMAT)
        client.send(f"[LIST] client {ADDR} receive the file names successfully".encode(FORMAT))
        namelist = namestr.split(" ")
        namelist.pop()
        if namelist[0] == "null":
            print("[LIST] Server dir is empty.")
            return
        for name in namelist:
            print(f"[LIST] {name}")
       

    def download(filenames):
        client.send("download".encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(msg)
        client.send(filenames.encode(FORMAT))
        # client is able to download more then one file once a time
        filenames = filenames.split(" ")
        for filename in filenames:
            file = open(PATH + "\\" + filename, 'w') 
            filedata = client.recv(SIZE).decode(FORMAT)
            if filedata == "NULL":
                print(f"[DOWNLOAD] File {filename} is not in Server dir.")
                client.send(f"[DOWNLOAD] File {filename} is not in Server dir.".encode(FORMAT))
            else:
                file.write(filedata)
                print(f"[DOWNLOAD] Client {ADDR} download the file {filename} sucessfully.")
                client.send(f"[DOWNLOAD] Client {ADDR} download the file {filename} sucessfully.".encode(FORMAT))

            file.close()
           
     
    def upload(filenames):
        client.send("upload".encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(msg)
        client.send(filenames.encode(FORMAT))
        # client is able to download more then one file once a time
        filenames = filenames.split(" ")
        for filename in filenames:
            file = open(PATH + "\\" + filename, 'r')
            filedata = file.read()
            if filedata == "":
                filedata = "NULL" # an empty string can not be sent   
            client.send(filedata.encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)
            print(msg)
            file.close()

    def build():
        filename = input("[BUILD] input the new file name:\n")
        file = open(PATH + '\\' + filename, 'w')
        print("[HELP] to mark the end of file, input ':q' ")
        data = input("[BUILD] input a row of data for this new file:\n")
        while not data == ":q":
            file.write(data + '\n')
            print("[BUILD] Successfully write a data into the file")
            data = input("[BUILD] input a row of data for this new file:\n")
        file.close()
        print(f"[BUILD] Successfully build the file: {filename}")
            

    def help():
        print("[HELP] you can input command like:") 
        print("[HELP] - help") # ask for help about the command 
        print("[HELP] - list") # list the file name (also directory name in server dir)
        print("[HELP] - build") # build a new file (so that you can upload it to server)
        print("[HELP] - download filename --statement: you can operate on more then one file, use blank space to seperate them.") # download a file from server
        print("[HELP] - upload filename --statement: you can operate on more then one file, use blank space to seperate them.") # upload a file to server
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
                print("[HELP] - download filename")
                continue
            else:
                download(command[9:])
        elif command.startswith('upload'):
            if len(command) < 8:
                print('[ERROR] Invalid command')
                print("[HELP] you can input command like:") 
                print("[HELP] - upload filename")
                continue
            else:
                upload(command[7:])
        elif command.startswith('exit'):
            client.send("exit".encode(FORMAT))
            break
        else:
            print('[ERROR] Invalid command')
            print("[HELP] you can input 'help' to get help.")
            continue
    client.send("[DISCONNECT] Client ask for disconnection.".encode(FORMAT))
    print("[DISCONNECT] Client ask for disconnection.")
    msg = client.recv(SIZE).decode(FORMAT)
    print(msg)
    client.send(f"[DISCONNECT] Client {ADDR} close connection.".encode(FORMAT))
    client.close()
    print("[DISCONNECT] Break the connection with server.")
    print("[EXIT] Byebye.")
    
if __name__ == '__main__':
    main()

