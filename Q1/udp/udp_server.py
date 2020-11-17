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

#Using the idea of TFTP protocol RFC 1350 to ensure reliabilty of UDP socket. 
#Using a combination of designated ACKs and timeouts to make that possible
while True:
    print("Waiting for File Name...")
    recvACK = b''
    file_name,ADDRESS = serverSocket.recvfrom(2048) #receiving the file name from client
    serverSocket.sendto(b'fname', ADDRESS)          # sending ACK to the client after receiving the file name
    recvACK,ADDRESS = serverSocket.recvfrom(100)    # receving the ACK from the client saying that client now knows that server has the filename
    while(recvACK != b'reack'):                     # If the received ACK gets lost some where, then repeat the whole proceduce
        try:
            # This is the most crucial part of this system
            serverSocket.settimeout(2)              # This timeout ensures that the server gets the filename and moves on even if any ack is lost.
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
        resACK = serverSocket.recv(100)            # Receiving ACK from the client after sending a chunk
        chunk = f.read(BUFSIZE)                    # Reading the file in chunks
        # Uncomment the next line to add a sleep of 100 us to the server after every packet trasfer
        # sleep(100/1000000)        
    f.close() 
    recvACK = b''
    # repeating the same procedure done while receving the filename, to send the EOF and receive the ACK from the client
    
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
    
    