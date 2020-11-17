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
total_file_size = 0
for message in messages:
    sendFileName.append(books[message])
    reveiveFileName.append("../received_files/udp/"+books[message].split("/")[-1][:-4] + "_UDP"+ "_" + str(os.getpid())+".txt")

connectionstart = time()
# Creating the socket
clientSocket = socket(AF_INET,SOCK_DGRAM)


for count in range(len(sendFileName)):
    #starting the timer 
    start = time()
    #Sending bookname to the server

    recvACK = b''
    # Corresponding logic for the server counter part, kindly look at server comments
    while(recvACK != b'fname'):
        clientSocket.sendto(sendFileName[count].encode(),ADDRESS) 
        recvACK,ADDRESS = clientSocket.recvfrom(100)
        clientSocket.sendto(b'reack',ADDRESS) 

    with open(reveiveFileName[count], "wb") as f:
        print("file opened") 
        
        while(True):
            # print("Receiving data ...")
            
            # clientSocket.settimeout(2)                 #starting the time for timeout
            chunk,ADDRESS = clientSocket.recvfrom(BUFSIZE) # Receiving the data in chunks of buffer size
            # print(ADDRESS)
            if not chunk or chunk == b'EOF':
                clientSocket.sendto(b'eofdone',ADDRESS) 
                break
                    
            f.write(chunk)
            clientSocket.sendto(b'ack',ADDRESS)

        # If timout occurs
    end = time()
    print("File received Successfully,...")
    print("Time Elapsed : {} seconds".format (end - start))
    file_size = (os.stat(sendFileName[count])).st_size
    total_file_size = total_file_size+file_size
    print("Througput is: {} bytes/sec".format((file_size)/(end-start)))
clientSocket.close()    
overallend = time()
print("overall Time Elapsed : {} seconds".format (overallend - connectionstart))
print("overall Througput is: {} bytes/sec".format((total_file_size)/(overallend-connectionstart)))