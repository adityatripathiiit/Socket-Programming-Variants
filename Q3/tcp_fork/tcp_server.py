from socket import * 
from math import ceil
import os
from time import time,sleep
import sys

hostIP = sys.argv[1]

serverPort = 12345      # Server IP(localhost)
BUFSIZE = 1024          # Buffer size     
HOST = hostIP    

ADDRESS = (HOST,serverPort)


#Creating the socket object
serverSocket = socket(AF_INET,SOCK_STREAM)

# uncomment the next line to disable Nagle's algorithm 
# serverSocket.setsockopt(IPPROTO_TCP, TCP_NODELAY, True)

# uncomment the next line to disable Delayed ACK  
# serverSocket.setsockopt(IPPROTO_TCP, TCP_QUICKACK, True)

#Binding to socket
serverSocket.bind(ADDRESS)

#Starting TCP listener
serverSocket.listen(1)

def handleRequest(clientSocket):
    file_name = clientSocket.recv(2048).decode()

    while(file_name):
        print("Connected")
        # Receiving filename from the client
        print(file_name)
        f = open(file_name, "rb")
        clientSocket.send(b'ack')
        resACK = clientSocket.recv(100)

        chunk = f.read(BUFSIZE)
        # print(ADDRESS)
        while(chunk):
            clientSocket.send(chunk)   # Sending the chunk to the client
            resACK = clientSocket.recv(100)
            chunk = f.read(BUFSIZE)    # Reading the file in chunks 
            # Uncomment the next line to add a sleep of 100 us to the server after every packet trasfer
        f.close() 
        clientSocket.send(b'EOF')
        print("successfully sent the file, closing the connection")
        file_name = clientSocket.recv(2048)

    clientSocket.close()


while True:
    
    print("Listening ...")
    #Starting the connection 
    clientSocket,ADDRESS = serverSocket.accept()
    clientSocket.settimeout(10)
    try:
        pid = os.fork()
    except OSError:
        exit("Could not create a child process")

    if(pid>0):
        continue
    else:
        print( "Client Is handled by process: ", os.getpid())
        handleRequest(clientSocket)
        exit()