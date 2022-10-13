'''
@File    :   TCPClient.py
@Time    :   2022/10/10 19:50:23
@Author  :   Zhang Maysion 
@Version :   1.0
@Contact :   zhangmx67@mail2.sysu.edu.cn
'''

import socket
import os
import datetime

# IP = socket.gethostbyname(socket.gethostname())
IP = 'LAPTOP-MAYSION'
# IP = 'Gulfira'
PORT = 12000
ADDR = (IP, PORT)
FORMAT = 'utf-8'
SIZE = 1024 
UPPERPATH = os.path.join(os.path.dirname(__file__), '..') # store the logfile in upper path
DIRPATH = UPPERPATH + "/CLIENT" 


def main():
    
    # below variables will be defined before real use
    logfile = None
    conn = None

    def addLog(log):
        logfile.write(log + '\n')
        print(log)


    def listRemote():
        conn.send("list".encode(FORMAT))
        namestr = conn.recv(SIZE).decode(FORMAT)
        conn.send(f"[LIST] client {ADDR} receive the file names successfully".encode(FORMAT))
        namelist = namestr.split(" ")
        namelist.pop()
        if namelist[0] == "null":
            addLog("[LIST] Server dir is empty.")
            return
        for name in namelist:
            addLog(f"[LIST] {name}")
       
    def listLocal():
        namelist = os.listdir(DIRPATH)
        for name in namelist:
            addLog(f"[LIST] {name}")



    def download(filenames):
        conn.send("download".encode(FORMAT))
        msg = conn.recv(SIZE).decode(FORMAT)
        addLog(msg)
        conn.send(filenames.encode(FORMAT))
        # client is able to download more then one file once a time
        filenames = filenames.split(" ")
        for filename in filenames:
            filedata = conn.recv(SIZE).decode(FORMAT)
            if filedata == "NULL":
                msg = f"[DOWNLOAD] File {filename} is not in Server dir."
            else:
                file = open(DIRPATH + "\\" + filename, 'w') 
                file.write(filedata)
                file.close()
                msg = f"[DOWNLOAD] Client {ADDR} download the file {filename} sucessfully."     
            addLog(msg)
            conn.send(msg.encode(FORMAT))
     
    def upload(filenames):
        conn.send("upload".encode(FORMAT))
        msg = conn.recv(SIZE).decode(FORMAT)
        addLog(msg)
        conn.send(filenames.encode(FORMAT))
        # client is able to download more then one file once a time
        filenames = filenames.split(" ")
        namelist = os.listdir(DIRPATH)
        for filename in filenames:
            if filename not in namelist:
                filedata = "NULL" # an empty string can not be sent
            else:
                file = open(DIRPATH + "\\" + filename, 'r')
                filedata = file.read()  
                file.close()
            conn.send(filedata.encode(FORMAT))
            msg = conn.recv(SIZE).decode(FORMAT)
            addLog(msg)
            

    def build():
        filename = input("[BUILD] input the new file name:\n")
        file = open(DIRPATH + '\\' + filename, 'w')
        print("[HELP] to mark the end of file, input ':q' ")
        data = input("[BUILD] input a row of data for this new file:\n")
        while not data == ":q":
            file.write(data + '\n')
            addLog("[BUILD] Successfully write a row of data into the file")
            data = input("[BUILD] input a row of data for this new file:\n")
        file.close()
        addLog(f"[BUILD] Successfully build the file: {filename}")
            

    def help():
        print("[HELP] you can input command like:") 
        print("[HELP] - help") # ask for help about the command 
        print("[HELP] - list local") # list the file name (also directory name in client dir)
        print("[HELP] - list remote") # list the file name (also directory name in server dir)
        print("[HELP] - build") # build a new file (so that you can upload it to server)
        print("[HELP] - download filename --statement: you can operate on more then one file, use blank space to seperate them.") # download a file from server
        print("[HELP] - upload filename --statement: you can operate on more then one file, use blank space to seperate them.") # upload a file to server
        print("[HELP] - exit") # exit the client
    

    # initialize:check the directory to store files
    logfile = open(UPPERPATH + '\\' + 'ClientLog.txt', 'a')
    logfile.write('\n')
    logfile.write(str(datetime.datetime.now()) + '\n') # record time
    addLog(f"[INITIALIZING] Check whether the directory {DIRPATH} exists")
    if not os.path.exists(DIRPATH):
        addLog(f"[CHECK] The directory {DIRPATH} does not exist")
        os.makedirs(DIRPATH)
        addLog(f"[MAKEDIR] the directory {DIRPATH} created")
    else:
        addLog(f"[CHECK] The directory {DIRPATH} exists")
    
    # connect to server
    addLog(f"[CONNECT] Ask a tcp connection")
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((ADDR))
    msg = conn.recv(SIZE).decode(FORMAT)
    addLog(msg)
    

    while True:
        command = input('[INPUT] input your command:\n')
        while len(command) < 4:
            addLog('[ERROR] Invalid command')
            print("[HELP] you can input 'help' to get help.")
            command = input('[INPUT] input your command:\n')
        if command.startswith('help'):
            help()
        elif command.startswith('list local'):
            listLocal()
        elif command.startswith('list remote'):
            listRemote()
        elif command.startswith('build'):
            build()
        elif command.startswith('download'):
            if len(command) < 10:
                addLog('[ERROR] Invalid command')
                print("[HELP] you can input command like:") 
                print("[HELP] - download filename")
                continue
            else:
                download(command[9:])
        elif command.startswith('upload'):
            if len(command) < 8:
                addLog('[ERROR] Invalid command')
                print("[HELP] you can input command like:") 
                print("[HELP] - upload filename")
                continue
            else:
                upload(command[7:])
        elif command.startswith('exit'):
            conn.send("exit".encode(FORMAT))
            break
        else:
            addLog('[ERROR] Invalid command')
            print("[HELP] you can input 'help' to get help.")
            continue
    conn.send("[DISCONNECT] Client ask for disconnection.".encode(FORMAT))
    addLog("[DISCONNECT] Client ask for disconnection.")
    msg = conn.recv(SIZE).decode(FORMAT)
    addLog(msg)
    conn.send(f"[DISCONNECT] Client {ADDR} close connection.".encode(FORMAT))
    conn.close()
    addLog("[DISCONNECT] Break the connection with server.")
    addLog("[EXIT] Byebye.")
    logfile.close()

def errorRecord(errorType):
    msg = '[ERROR] ' + errorType
    print(msg)
    logfile = open(UPPERPATH + '\\' + 'ServerLog.txt', 'a')
    logfile.write(msg)
    logfile.close()

if __name__ == '__main__':
    try:
        main()
    except ConnectionRefusedError:
        errorRecord('Connection Refused Error')
    except OSError:
        errorRecord('OS Error')