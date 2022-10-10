'''
@File    :   TCPServer.py
@Time    :   2022/10/10 19:45:30
@Author  :   Zhang Maysion 
@Version :   1.0
@Contact :   zhangmx67@mail2.sysu.edu.cn
'''


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
    
    # first recv a number
    
    
    
    
    last_time = time.localtime(time.time())
    cur_time = time.localtime(time.time())
    # each time client end a connection will renew the time
    # >=20 second not appear new connection ask, then print logs and exit

    def list():
        pass


    def download():
        pass


    def upload():
        pass


    def printLogs():
        pass


    # initialize
    logs.append(f"[INITIALIZING] Check whether the directory {PATH} exists")
    if not os.path.exists(PATH):
        logs.append(f"[CHECK] The directory {PATH} does not exist")
        os.makedirs(PATH)
        logs.append(f"[MAKEDIR] the directory {PATH} created")
    else:
        logs.append(f"[CHECK] The directory {PATH} exists")

    logs.append('[STARTING] Server is starting.')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    logs.append('[LISTENING] Server is listening.')
    last_time = time.localtime(time.time())
    
    while True:
        conn, addr = server.accept()
        conn.send("Connect sucessfully".encode(FORMAT))

        logs.append(f"[NEW CONNECTION] {addr} connected.")

        filename = conn.recv(SIZE).decode(FORMAT)
        logs.append("[RECV] Filename received.")
        file = open(PATH+'\\'+filename, "w")
        conn.send("Filename is received.".encode())

        data = conn.recv(SIZE).decode(FORMAT)
        logs.append(f"[RECV] File data received.")
        file.write(data)
        conn.send("File data received.".encode(FORMAT))  

        file.close()
        conn.close()    
        logs.append(f"[DISCONNECTED] {addr} disconnected.")  

        last_time = time.localtime(time.time())
        

    for log in logs:
        print(log)
        logfile.write(log + '\n')
    logfile.close()

if __name__ == '__main__':
    main()