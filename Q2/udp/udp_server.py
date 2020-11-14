from socket import *
import os
from time import time,sleep
from math import ceil 
import sys 

serverPort = 12345  # Server IP(localhost)
BUFSIZE = 32        # Buffer size     
HOST = ""
ADDRESS = (HOST,serverPort)

serverSocket = socket(AF_INET,SOCK_DGRAM) #creating the socket

serverSocket.bind(ADDRESS)


while True:
    print("Waiting for File Name...")
    file_name,ADDRESS = serverSocket.recvfrom(2048) #receiving the file name from client
    start = time()                                  # Starting timer
    file_name  = file_name.decode()
    f = open(file_name,"rb")
    chunk = f.read(BUFSIZE)
    # print(ADDRESS)
    while(chunk):
        serverSocket.sendto(chunk,ADDRESS)         # sending the chunks of the file to the client
        chunk = f.read(BUFSIZE)                    # Reading the file in chunks
        # Uncomment the next line to add a sleep of 100 us to the server after every packet trasfer
        # sleep(100/1000000)    
        
    f.close() 
    print("successfully sent the file")
    end = time()
    print("Time Elapsed : {} seconds".format (end - start))

serverSocket.close()
    
    