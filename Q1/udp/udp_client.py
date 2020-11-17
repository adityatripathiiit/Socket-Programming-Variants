from socket import *
import os
import sys
from time import time 


BUFSIZE = 1024                       # Buffer size
serverName = "127.0.0.1"            # Server IP(localhost)
serverPort = 12345                  # Server Port number
ADDRESS = (serverName, serverPort)  # forming tuple of server IP and port
TIMEOUT = 2                         # Defining timeout (in seconds) for UDP client to timeout the connection after give seconds of inactivity


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
    reveiveFileName.append("../received_files/udp/"+books[message].split("/")[-1][:-4] + "_UDP"+ "_" + str(os.getpid())+".txt")

# Creating the socket
clientSocket = socket(AF_INET,SOCK_DGRAM)

for count in range(len(sendFileName)):
    #starting the timer 
    start = time()
    #Sending bookname to the server

    recvACK = b''
    while(recvACK != b'fname'):
        clientSocket.sendto(sendFileName[count].encode(),ADDRESS) 
        recvACK,ADDRESS = clientSocket.recvfrom(100)
        clientSocket.sendto(b'reack',ADDRESS) 

    with open(reveiveFileName[count], "wb") as f:
        print("file opened") 
        
        while(True):
            # print("Receiving data ...")
            try:
                # clientSocket.settimeout(2)                 #starting the time for timeout
                chunk,ADDRESS = clientSocket.recvfrom(BUFSIZE) # Receiving the data in chunks of buffer size
                # print(ADDRESS)
                if not chunk or chunk == b'EOF':
                    clientSocket.sendto(b'eofdone',ADDRESS) 
                    break
                        
                f.write(chunk)
                clientSocket.sendto(b'ack',ADDRESS)
            except timeout:
                print('time out')
                break
            

        # If timout occurs
    print("File received Successfully, closing the connection ...")
    end = time()
    print("Time Elapsed : {} seconds".format (end - start))
clientSocket.close()    