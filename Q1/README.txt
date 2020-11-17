
The folder structure is as follows: 

.
└── Q1/
    ├── novels/
    │   ├── Heartsease.txt
    │   ├── Roget’s Thesaurus.txt
    │   ├── The 1991 CIA World Factbook.txt
    │   ├── The Conquest Of Peru.txt
    │   └── War and Peace.txt
    ├── received_files/
    │   ├── tcp/
    │   │   └── tcpfiles
    │   └── udp/
    │       └── udpfiles
    ├── tcp/
    │   ├── tcp_client.py
    │   └── tcp_server.py
    ├── udp/
    │   ├── udp_client.py
    │   └── udp_server.py
    └── README.txt
    



To run the TCP server, go to the tcp folder and run the command python3 tcp_server.py

To run the TCP client, go to the tcp folder and run the command python3 tcp_client.py. This will give the user options to send specific files. Those files can be selected and send.  
Enter the number of files required as a string seperated by a space. For example, if clients wants book number 1,2 and 4 then provide 1 2 4 as an input. For all the files, provide 1 2 3 4 5 as input. 


The same instructions goes for the UDP client and UDP server. 

