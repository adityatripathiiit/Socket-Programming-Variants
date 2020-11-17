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

connectionstart = time()
#Creating client socket
clientSocket = socket(AF_INET,SOCK_STREAM)


clientSocket.connect(ADDRESS) # 3 whay handshake's first handshake,i.e connection setup 

connectionsetup = time()

print("connection setup time : {} seconds".format (connectionsetup - connectionstart))
total_file_size = 0

for count in range(len(sendFileName)):
    start = time()
    #sending the corresponding file name 
    clientSocket.send(sendFileName[count].encode())
    # Receiving ACK for the sent packet
    recvACK = clientSocket.recv(100)                
    # Sending ACK to the server
    clientSocket.send(b'ack')

    with open(reveiveFileName[count], "wb") as f:
        print("file opened")
        while(True):
            chunk = clientSocket.recv(BUFSIZE) # receiving the file in chunks of buffer size
            if not chunk or chunk == b'EOF':   # If the EOF received then end the file transfer
                break 
            f.write(chunk)                     # Writing the chunk to the file
            clientSocket.send(b'ack')          # seniding ACK to the server after receiving the chunk, marking
                                               # that it is available for receiving other chunks
    f.close()
    end = time()
    
    print("File received Successfully, closing the connection ...")
    print("Time Elapsed : {} seconds".format (end - start))
    file_size = (os.stat(sendFileName[count])).st_size
    total_file_size = total_file_size+file_size
    print("Througput is: {} bytes/sec".format((file_size)/(end-start)))
clientSocket.close() #closing the connection

overallend = time()
print("overall Time Elapsed : {} seconds".format (overallend - connectionstart))
print("overall Througput is: {} bytes/sec".format((total_file_size)/(overallend-connectionstart)))