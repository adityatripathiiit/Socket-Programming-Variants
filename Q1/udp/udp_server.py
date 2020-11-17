from socket import *
import os
from time import time,sleep
from math import ceil 
import sys 

serverPort = 12345  # Server IP(localhost)
BUFSIZE = 1024       # Buffer size     
HOST = ""
ADDRESS = (HOST,serverPort)

serverSocket = socket(AF_INET,SOCK_DGRAM) #creating the socket

serverSocket.bind(ADDRESS)


while True:
    print("Waiting for File Name...")
    recvACK = b''
    file_name,ADDRESS = serverSocket.recvfrom(2048) #receiving the file name from client
    serverSocket.sendto(b'fname', ADDRESS)
    recvACK,ADDRESS = serverSocket.recvfrom(100)
    while(recvACK != b'reack'):
        try:
            serverSocket.settimeout(2)
            file_name,ADDRESS = serverSocket.recvfrom(2048) #receiving the file name from client
            serverSocket.sendto(b'fname', ADDRESS)
            recvACK,ADDRESS = serverSocket.recvfrom(100)
        except timeout:
            break

    
    file_name  = file_name.decode()
    f = open(file_name,"rb")
    chunk = f.read(BUFSIZE)
    # print(ADDRESS)
    while(chunk):
        serverSocket.sendto(chunk,ADDRESS)         # sending the chunks of the file to the client
        resACK = serverSocket.recv(100)
        chunk = f.read(BUFSIZE)                    # Reading the file in chunks
        # Uncomment the next line to add a sleep of 100 us to the server after every packet trasfer
        # sleep(100/1000000)        
    f.close() 
    recvACK = b''
    serverSocket.sendto(b'EOF', ADDRESS)
    recvACK, ADDRESS = serverSocket.recvfrom(100)
    while(recvACK != b'eofdone'):
        try:
            serverSocket.settimeout(2)
            serverSocket.sendto(b'EOF', ADDRESS)
            recvACK, ADDRESS = serverSocket.recvfrom(100)
        except timeout:
            break
    print("successfully sent the file")

serverSocket.close()
    
    