'''
@File    :   TCPServer.py
@Time    :   2022/10/10 19:45:30
@Author  :   Zhang Maysion 
@Version :   1.0
@Contact :   zhangmx67@mail2.sysu.edu.cn
'''


from pickle import FROZENSET
import socket
import os
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 12000
ADDR = (IP, PORT)
SIZE = 2048
FORMAT = 'utf-8'
PATH = "SERVER" 


def main():
    logfile = open('Log.txt', 'a') # append the logfile
    logs = [] # use a list to store new logs
    

    def addLog(log):
        logfile.write(log + '\n')
        print(log)

    
    def list(conn, addr):
        namelist = os.listdir(PATH)
        namestr = ""
        for name in namelist:
            namestr = namestr + name + " "
        addLog("[LIST] Send the list of filename in server dir to client.")
        if len(namelist) == 0:
            conn.send("null ".encode(FORMAT)) # a length(0) string can not be sent,use null instead
        conn.send(namestr.encode(FORMAT))
        msg = conn.recv(SIZE).decode(FORMAT)
        addLog(msg)


    def download(conn, addr):
        conn.send("[DOWNLOAD] Server is ready to upload files".encode(FORMAT))
        filenames = conn.recv(SIZE).decode(FORMAT)
        # client is able to download more then one file once a time
        filenames = filenames.split(" ")
        for filename in filenames:
            file = open(PATH + "\\" + filename, 'r')
            filedata = file.read()
            conn.send(filedata.encode(FORMAT))
            msg = conn.recv(SIZE).decode(FORMAT)
            addLog(msg)
            file.close()

   

    def upload(conn, addr):
        conn.send("[UPLOAD] Server is ready to receive files.".encode(FORMAT)) 
        filenames = conn.recv(SIZE).decode(FORMAT)
        conn.send("[UPLOAD] Server receive file names successfully.".encode(FORMAT)) 
        # client is able to download more then one file once a time
        filenames = filenames.split(" ")
        for filename in filenames:
            file = open(PATH + "\\" + filename, 'w') 
            filedata = conn.recv(SIZE).decode(FORMAT)
            if filedata != "NULL":
                file.write(filedata)
            file.close()
            addLog(f"[UPLOAD] Client {ADDR} upload the file {filename} sucessfully.")
            conn.send(f"[UPLOAD] Client {ADDR} upload the file {filename} sucessfully.".encode(FORMAT))
       

    # initialize
    addLog(f"[INITIALIZING] Check whether the directory {PATH} exists")
    if not os.path.exists(PATH):
        addLog(f"[CHECK] The directory {PATH} does not exist")
        os.makedirs(PATH)
        addLog(f"[MAKEDIR] the directory {PATH} created")
    else:
        addLog(f"[CHECK] The directory {PATH} exists")

    addLog('[STARTING] Server is starting.')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    addLog('[LISTENING] Server is listening.')
    
     
    # the first loop is for new connection
    # the second loop is for new command in each connection
    while True:
        conn, addr = server.accept()
        conn.send("[STATUS] Connect to server successfully.".encode(FORMAT))
        addLog(f"[NEW CONNECTION] {addr} connected.")
        # first recv a msg to get the kind of function
        functionType = conn.recv(SIZE).decode(FORMAT)
        while True:
            if functionType.startswith("list"):
                list(conn, addr)
            elif functionType.startswith("download"):
                download(conn, addr)
            elif functionType.startswith("upload"):
                upload(conn, addr)
            elif functionType.startswith("exit"):
                break
            functionType = conn.recv(SIZE).decode(FORMAT)
        # disconnect
        msg = conn.recv(SIZE).decode(FORMAT)
        addLog(msg)
        conn.send("[DISCONNECTION] Server is ready to disconnect".encode(FORMAT))
        msg = conn.recv(SIZE).decode(FORMAT)
        addLog(msg)
        conn.close()
        addLog("[DISCONNECTION] Success.")
        
    

if __name__ == '__main__':
    main()