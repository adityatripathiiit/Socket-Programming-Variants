from socket import *
import os
from time import time 
import sys 

BUFSIZE = 1024                     # Buffer size
serverName = "127.0.0.1"           # Server IP(localhost)
serverPort = 12345                 # Server Port number
ADDRESS = (serverName, serverPort) # forming tuple of server IP and port

books = {"1": "../novels/Heartsease.txt", "2": "../novels/Roget’s Thesaurus.txt", "3": "../novels/The 1991 CIA World Factbook.txt", "4":"../novels/The Conquest Of Peru.txt", "5": "../novels/War and Peace.txt"}
print("Select the book you want to request from the server, from the following list of books: ")
print("1: Heartsease")
print("2: Roget's Thesaurus")
print("3: The 1991 CIA World Factbook")
print("4: The Conquest Of Peru")
print("5: War and Peace")

messages = list(input("Enter the book Numbers seperated by space: ").split())

for message in messages:
    if (message not in books.keys()):
        print("Please choose a valid book number") 
        sys.exit()

sendFileName = []
reveiveFileName= []
for message in messages:
    sendFileName.append(books[message])
    reveiveFileName.append("../received_files/tcp/"+books[message].split("/")[-1][:-4] + "_TCP"+ "_" + str(os.getpid())+".txt")

#Creating client socket
clientSocket = socket(AF_INET,SOCK_STREAM)

# uncomment the next line to disable Nagle's algorithm 
# clientSocket.setsockopt(IPPROTO_TCP, TCP_NODELAY, True)

# uncomment the next line to disable Delayed ACK  
# clientSocket.setsockopt(IPPROTO_TCP, TCP_QUICKACK, True)

#starting the timer

clientSocket.connect(ADDRESS) # 3 whay handshake's first handshake,i.e connection setup 

# Sending the server, name of the book
# clientSocket.send(str(len(sendFileName)).encode())

for count in range(len(sendFileName)):
    start = time()
    
    clientSocket.send(sendFileName[count].encode())

    recvACK = clientSocket.recv(100)

    clientSocket.send(b'ack')

    with open(reveiveFileName[count], "wb") as f:
        print("file opened")
        try:
            while(True):
                chunk = clientSocket.recv(BUFSIZE) # receiving the file in chunks of buffer size
                if not chunk or chunk == b'EOF':
                    break 
                f.write(chunk)                     # Writing the chunk to the file
                clientSocket.send(b'ack')
        except:
            print("An exception occured")
    f.close()
    end = time()
    
    print("File received Successfully, closing the connection ...")
    print("Time Elapsed : {} seconds".format (end - start))
    print("Througput is: {} bytes/sec".format((os.stat(sendFileName[count]).st_size)/(end-start)))
clientSocket.close() #closing the connection