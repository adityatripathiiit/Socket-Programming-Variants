
The folder structure is as follows: 

.
└── TCP_UDP_File_Transfer/
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


The same instructions goes for the UDP client and UDP server. 

To disable nagle's algorithm in TCP server uncomment line 21  in tcp_sever.py.


To disable nagle's algorithm in TCP client uncomment line 29 in tcp_client.py.


To disable delayed ACK in TCP server uncomment line 24 in tcp_server.py


To disable delayed ACK in TCP client uncomment line 32 in tcp_client.py


Buffersize can be changed in clients and servers of both tcp and udp, by changing the global variable BUFSIZE. 


To add sleep of 100 us in TCP server uncomment line 48 in tcp_server.py

To add sleep of 100 us in UDP server uncomment line 29 in udp_server.py
