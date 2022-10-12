'''
@File    :   TCPServer.py
@Time    :   2022/10/10 19:45:30
@Author  :   Zhang Maysion 
@Version :   1.0
@Contact :   zhangmx67@mail2.sysu.edu.cn
'''

import socket
import os


# IP = socket.gethostbyname(socket.gethostname())
IP = 'LAPTOP-MAYSION'
PORT = 12000
ADDR = (IP, PORT)
SIZE = 2048
FORMAT = 'utf-8'
PATH = "SERVER" 


def main():
    
    def addLog(logfile, log):
        logfile.write(log + '\n')
        print(log)

    
    def list(conn, addr):
        namelist = os.listdir(PATH)
        namestr = ""
        for name in namelist:
            namestr = namestr + name + " "
        addLog(logfile, "[LIST] Send the list of filename in server dir to client.")
        if len(namelist) == 0:
            conn.send("null ".encode(FORMAT)) # a length(0) string can not be sent,use null instead
        conn.send(namestr.encode(FORMAT))
        msg = conn.recv(SIZE).decode(FORMAT)
        addLog(logfile, msg)


    def download(conn, addr):
        conn.send("[DOWNLOAD] Server is ready to upload files".encode(FORMAT))
        filenames = conn.recv(SIZE).decode(FORMAT)
        # client is able to download more then one file once a time
        filenames = filenames.split(" ")
        namelist = os.listdir(PATH)
        for filename in filenames:
            if filename in namelist:
                file = open(PATH + "\\" + filename, 'r')
                filedata = file.read()
                file.close()
            else:
                filedata = 'NULL'
            conn.send(filedata.encode(FORMAT))
            msg = conn.recv(SIZE).decode(FORMAT)
            addLog(logfile, msg)

   
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
            addLog(logfile, f"[UPLOAD] Client {ADDR} upload the file {filename} sucessfully.")
            conn.send(f"[UPLOAD] Client {ADDR} upload the file {filename} sucessfully.".encode(FORMAT))
       

    # initialize
    logfile = open('Log.txt', 'a')
    addLog(logfile, f"[INITIALIZING] Check whether the directory {PATH} exists")
    if not os.path.exists(PATH):
        addLog(logfile, f"[CHECK] The directory {PATH} does not exist")
        os.makedirs(PATH)
        addLog(logfile, f"[MAKEDIR] the directory {PATH} created")
    else:
        addLog(logfile, f"[CHECK] The directory {PATH} exists")

    addLog(logfile, '[STARTING] Server is starting.')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    addLog(logfile, '[LISTENING] Server is listening.')
    logfile.close()
    
     
    # the first loop is for new connection
    # the second loop is for new command in each connection
    while True:
        logfile = open('Log.txt', 'a')
        conn, addr = server.accept()
        conn.send("[STATUS] Connect to server successfully.".encode(FORMAT))
        addLog(logfile, f"[NEW CONNECTION] {addr} connected.")
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
        addLog(logfile, msg)
        conn.send("[DISCONNECTION] Server is ready to disconnect".encode(FORMAT))
        msg = conn.recv(SIZE).decode(FORMAT)
        addLog(logfile, msg)
        conn.close()
        addLog(logfile, "[DISCONNECTION] Success.")
        logfile.close()
        
    

if __name__ == '__main__':
    main()