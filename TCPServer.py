'''
@File    :   TCPServer.py
@Time    :   2022/10/10 19:45:30
@Author  :   Zhang Maysion 
@Version :   1.0
@Contact :   zhangmx67@mail2.sysu.edu.cn
'''


import socket
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 12000
ADDR = (IP, PORT)
SIZE = 2048
FORMAT = 'utf-8'
PATH = "SERVER"


def main():
    logfile = open('Log.txt', 'a') # append the logfile
    logs = [] # use a list to store new logs

    def list():
        pass

    def download():
        pass

    def upload():
        pass


    def printLogs():
        pass



    print(f"[INITIALIZING] Check whether the directory {PATH} exists")
    if not os.path.exists(PATH):
        print(f"[CHECK] The directory {PATH} does not exist")
        os.makedirs(PATH)
        print(f"[MAKEDIR] the directory {PATH} created")
    else:
        print(f"[CHECK] The directory {PATH} exists")

    print('[STARTING] Server is starting.')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print('[LISTENING] Server is listening.')

    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")

        filename = conn.recv(SIZE).decode(FORMAT)
        print("[RECV] Filename received.")
        file = open(PATH+'\\'+filename, "w")
        conn.send("Filename is received.".encode())

        data = conn.recv(SIZE).decode(FORMAT)
        print(f"[RECV] File data received.")
        file.write(data)
        conn.send("File data received.".encode(FORMAT))  

        file.close()
        conn.close()    
        print(f"[DISCONNECTED] {addr} disconnected.")  


    for log in logs:
        logfile.write(log + '\n')
    logfile.close()

if __name__ == '__main__':
    main()