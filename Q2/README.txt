
The folder structure is as follows: 

.
└── Q2/
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
    ├── tcp_fork/
    │   ├── client_run.sh
    │   ├── tcp_client_non_persistent.py.py
    │   ├── tcp_client_persistent.py.py
    │   └── tcp_server.py
    ├── tcp_thread/
    │   ├── client_run.sh
    │   ├── tcp_client_non_persistent.py.py
    │   ├── tcp_client_persistent.py.py
    │   └── tcp_server.py
    └── README.txt
    



To run the TCP server, go to the tcp folder and run the command python3 tcp_server.py

To run all the clients concurrently, run the script client_run.sh, use the command "sudo sh ./client_run.sh" to run the client. 

Otherwise, just as previous instructions, run any python file and provide the input as required. 


