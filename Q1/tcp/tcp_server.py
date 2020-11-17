from socket import * 
from math import ceil
import os
from time import time,sleep
import sys


serverPort = 12345      # Server IP(localhost)
BUFSIZE = 1024          # Buffer size     
HOST = ""               

ADDRESS = (HOST,serverPort)


#Creating the socket object
serverSocket = socket(AF_INET,SOCK_STREAM)

#Binding to socket
serverSocket.bind(ADDRESS)

#Starting TCP listener
serverSocket.listen(1)

while True:
    
    print("Listening ...")
    #Starting the connection 
    clientSocket,ADDRESS = serverSocket.accept()
    clientSocket.settimeout(10)
    file_name = clientSocket.recv(2048).decode()

    while(file_name):
        print("Connected")
        # Receiving filename from the client
        print(file_name)
        f = open(file_name, "rb")
        #sending ACK to client after receiving file name from client
        clientSocket.send(b'ack')
        #Receiving ACK back from the Client confirming that it knows that server has the filename
        resACK = clientSocket.recv(100)

        chunk = f.read(BUFSIZE)
        # print(ADDRESS)
        while(chunk):
            clientSocket.send(chunk)   # Sending the chunk to the client
            resACK = clientSocket.recv(100) #receving ack for the chunk send to client
            chunk = f.read(BUFSIZE)    # Reading the file in chunks 
            
        f.close() 
        clientSocket.send(b'EOF')      # Sending a EOF packet to mark the end of a file transfer
        print("successfully sent the file, closing the connection")
        file_name = clientSocket.recv(2048) # Receiving name of the file again from the client

    clientSocket.close()
    
    