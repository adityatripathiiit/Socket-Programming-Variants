from socket import *
import os
import sys
from time import time 


BUFSIZE = 32                        # Buffer size
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

message = input("Enter the book Number: ")

while (message not in books.keys()):
    print("Please choose a valid book number") 
    message = input("Enter the book Number: ")

# Creating the socket
clientSocket = socket(AF_INET,SOCK_DGRAM)
#starting the timer 
start = time()
#Sending bookname to the server
clientSocket.sendto(books[message].encode(),ADDRESS) 


fileName = "../received_files/udp/"+books[message].split("/")[-1][:-4] + "_UDP"+ "_" + str(os.getpid())+".txt"

with open(fileName, "wb") as f:
    print("file opened") 
    try:
        while(True):
            # print("Receiving data ...")
            clientSocket.settimeout(TIMEOUT)               #starting the time for timeout
            chunk,ADDRESS = clientSocket.recvfrom(BUFSIZE) # Receiving the data in chunks of buffer size
            # print(ADDRESS)
            f.write(chunk)
    except timeout:
        # If timout occurs
        f.close()
        print("File received Successfully, closing the connection ...")
        clientSocket.close()
        end = time()
        print("Time Elapsed : {} seconds".format (end - start -TIMEOUT))
        