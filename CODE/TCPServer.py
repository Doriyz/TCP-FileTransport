'''
@File    :   TCPServer.py
@Time    :   2022/10/10 19:45:30
@Author  :   Zhang Maysion 
@Version :   1.0
@Contact :   zhangmx67@mail2.sysu.edu.cn
'''

import socket
import os
import datetime

# IP = socket.gethostbyname(socket.gethostname())
IP = 'LAPTOP-MAYSION'
PORT = 12000
ADDR = (IP, PORT)
SIZE = 2048
FORMAT = 'utf-8'
UPPERPATH = os.path.join(os.path.dirname(__file__), '..') # store the logfile in upper path
DIRPATH = UPPERPATH + "/SERVER" 


def main():
    
    # below variables will be defined before real use
    logfile = None 
    conn = None
    addr = None
    

    def addLog(log):
        logfile.write(log + '\n')
        print(log)

    
    def list():
        namelist = os.listdir(DIRPATH)
        namestr = ""
        for name in namelist:
            namestr = namestr + name + " "
        addLog("[LIST] Send the list of filename in server dir to client.")
        if len(namelist) == 0:
            conn.send("null ".encode(FORMAT)) # a length(0) string can not be sent,use null instead
        conn.send(namestr.encode(FORMAT))
        msg = conn.recv(SIZE).decode(FORMAT)
        addLog(msg)


    def download():
        conn.send("[DOWNLOAD] Server is ready to upload files".encode(FORMAT))
        filenames = conn.recv(SIZE).decode(FORMAT)
        # client is able to download more then one file once a time
        filenames = filenames.split(" ")
        namelist = os.listdir(DIRPATH)
        for filename in filenames:
            if filename in namelist:
                file = open(DIRPATH + "\\" + filename, 'r')
                filedata = file.read()
                file.close()
            else:
                filedata = 'NULL'
            conn.send(filedata.encode(FORMAT))
            msg = conn.recv(SIZE).decode(FORMAT)
            addLog(msg)

   
    def upload():
        conn.send("[UPLOAD] Server is ready to receive files.".encode(FORMAT)) 
        filenames = conn.recv(SIZE).decode(FORMAT)
        conn.send("[UPLOAD] Server receive file names successfully.".encode(FORMAT)) 
        # client is able to download more then one file once a time
        filenames = filenames.split(" ")
        for filename in filenames:
            filedata = conn.recv(SIZE).decode(FORMAT)
            if filedata != "NULL":
                file = open(DIRPATH + "\\" + filename, 'w')    
                file.write(filedata)
                file.close()
                addLog(f"[UPLOAD] Client {ADDR} upload the file {filename} sucessfully.")
                conn.send(f"[UPLOAD] Client {ADDR} upload the file {filename} sucessfully.".encode(FORMAT))
       

    # initialize
    logfile = open(UPPERPATH + '\\' + 'ServerLog.txt', 'a')
    logfile.write('\n')
    logfile.write(str(datetime.datetime.now()) + '\n') # record time
    addLog(f"[INITIALIZING] Check whether the directory {DIRPATH} exists")
    if not os.path.exists(DIRPATH):
        addLog(f"[CHECK] The directory {DIRPATH} does not exist")
        os.makedirs(DIRPATH)
        addLog(f"[MAKEDIR] the directory {DIRPATH} created")
    else:
        addLog(f"[CHECK] The directory {DIRPATH} exists")

    addLog('[STARTING] Server is starting.')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    addLog('[LISTENING] Server is listening.')
    logfile.close()
    
     
    # the first loop is for new connection
    # the second loop is for new command in each connection
    while True:
        conn, addr = server.accept()
        logfile = open(UPPERPATH + '\\' + 'ServerLog.txt', 'a')
        conn.send("[STATUS] Connect to server successfully.".encode(FORMAT))
        addLog(f"[NEW CONNECTION] {addr} connected.")
        # first recv a msg to get the kind of function
        functionType = conn.recv(SIZE).decode(FORMAT)
        while True:
            if functionType.startswith("list"):
                list()
            elif functionType.startswith("download"):
                download()
            elif functionType.startswith("upload"):
                upload()
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
        logfile.close()
        
def errorRecord(errorType):
    msg = '[ERROR] ' + errorType
    print(msg)
    logfile = open(UPPERPATH + '\\' + 'ServerLog.txt', 'a')
    logfile.write(msg + '\n')
    logfile.close()


if __name__ == '__main__':
    try:
        main()
    except ConnectionResetError:
        errorRecord('Connection Reset Error')
    except OSError:
        errorRecord('OS Error')