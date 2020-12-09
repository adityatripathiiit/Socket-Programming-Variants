# Socket-Programming-Variants ⭐

File transfer over TCP/UDP sockets with network programming on mininet and various models. Contains client and server programs that enable to download multiple files on a same/single TCP/UDP connection. Also a Mininet network, where you instantiate different desired (parameterized) topologies, where one of the host node acts as server and subset of the remaining nodes act as a clients.


## Codebase Directory Architecture: 📁

```
Socket-Programming-Variants
├─ custom_network_topology
│  ├─ mininet_variants
│  │  ├─ Tree_custom_Link_Bandwidth.py
│  │  ├─ Tree_custom_Link_Loop.py
│  │  └─ Tree_custom_Link_Scaling_Load.py
│  ├─ novels
│  │  ├─ Heartsease.txt
│  │  ├─ Roget’s Thesaurus.txt
│  │  ├─ The 1991 CIA World Factbook.txt
│  │  ├─ The Conquest Of Peru.txt
│  │  └─ War and Peace.txt
│  ├─ README.txt
│  ├─ received_files
│  │  └─ tcp
│  │     └─ Heartsease_TCP_268651.txt
│  ├─ tcp_fork
│  │  ├─ tcp_client_non_persistent.py
│  │  ├─ tcp_client_persistent.py
│  │  └─ tcp_server.py
│  └─ tcp_thread
│     ├─ tcp_client_non_persistent.py
│     ├─ tcp_client_persistent.py
│     └─ tcp_server.py
├─ fork_thread_server
│  ├─ novels
│  │  ├─ Heartsease.txt
│  │  ├─ Roget’s Thesaurus.txt
│  │  ├─ The 1991 CIA World Factbook.txt
│  │  ├─ The Conquest Of Peru.txt
│  │  └─ War and Peace.txt
│  ├─ README.txt
│  ├─ received_files
│  │  └─ tcp
│  │     └─ Heartsease_TCP_268651.txt
│  ├─ tcp_fork
│  │  ├─ client_run.sh
│  │  ├─ tcp_client_non_persistent.py
│  │  ├─ tcp_client_persistent.py
│  │  └─ tcp_server.py
│  └─ tcp_thread
│     ├─ client_run.sh
│     ├─ tcp_client_non_persistent.py
│     ├─ tcp_client_persistent.py
│     └─ tcp_server.py
├─ mininet_migration
│  ├─ mininet_variants
│  │  ├─ linear_switch_bandwidth.py
│  │  ├─ linear_switch_delay.py
│  │  ├─ linear_switch_hops.py
│  │  ├─ linear_switch_loss.py
│  │  ├─ single_switch_diff_file.py
│  │  └─ single_switch_same_file.py
│  ├─ novels
│  │  ├─ Heartsease.txt
│  │  ├─ Roget’s Thesaurus.txt
│  │  ├─ The 1991 CIA World Factbook.txt
│  │  ├─ The Conquest Of Peru.txt
│  │  └─ War and Peace.txt
│  ├─ README.txt
│  ├─ received_files
│  │  └─ tcp
│  │     └─ Heartsease_TCP_268651.txt
│  ├─ tcp_fork
│  │  ├─ tcp_client_non_persistent.py
│  │  ├─ tcp_client_persistent.py
│  │  └─ tcp_server.py
│  └─ tcp_thread
│     ├─ tcp_client_non_persistent.py
│     ├─ tcp_client_persistent.py
│     └─ tcp_server.py
├─ persistent_connection
│  ├─ novels
│  │  ├─ Heartsease.txt
│  │  ├─ Roget’s Thesaurus.txt
│  │  ├─ The 1991 CIA World Factbook.txt
│  │  ├─ The Conquest Of Peru.txt
│  │  └─ War and Peace.txt
│  ├─ README.txt
│  ├─ received_files
│  │  ├─ tcp
│  │  │  └─ Heartsease_TCP_268651.txt
│  │  └─ udp
│  │     └─ Heartsease_UDP_268651.txt
│  ├─ tcp
│  │  ├─ tcp_client.py
│  │  └─ tcp_server.py
│  └─ udp
│     ├─ udp_client.py
│     └─ udp_server.py
└─ README.md

```





## Features checklist ✅

```
✅ Client-Server Architecture
✅ File transfer over TCP socket 
✅ File transfer over UDP Socket
✅ Persistent UDP file transfer [TFTP protocol RFC 1350]
✅ Persistent TCP file transfer
✅ Multithreaded Server using forking and threading 
✅ Multirequest client 
✅ Client and server programs that enable to download multiple files on a same/single TCP/UDP connection
✅ Mininet migration of various models on custom topologies and prebuilt topologies(linear, tree etc) with custom configured network parameters. 

```

## Instructions to Run :runner:

- There are instructions on how to run the programs inside each subdirectory of this repository. Please refer to those

## Changes required to create a persistent connection over 🚀
---
- ### TCP
    * On the Client-side:
        - ACK is sent and received after send the requested filename
        - ACK is sent after receiving every chunk of file from the server.
        - If the chunk says “EOF” in binary, then this means that the server sends the
        signal that the current file has ended and all the further data will not be a part
        of this file. This “EOF” is sent from the server.
        This process is repeated for all the files requested.
    * On the Server-side:
        - Apart from all the corresponding acks receiving and sending from the client,
        the server sent an “EOF” signal to mark the end of the sending file
--- 
- ### UDP 

    - UDP is connectionless protocol. Therefore talking about connection does notmake sense in UDP. But for this part, we have considered transferring all the files on a single formed socket. 

    - Here we tried to convert UDP to a reliable model using inspiration from TCP and TFTP protocol RFC 1350. We used techniques such as sending ACK’s and resending of the packets, in combination with timeouts to achieve the working of this model.

    - The most important places that we needed to ensure reliability was while
    sending the name of the file to be fetched and while marking the end of a
    receiving file.
    - To ensure this, at both the places we kept on sending ACKs from both the
    server and the client, until and unless, one of them does not get the required
    information. And the other one is handled with carefully placed timeouts. Here
    
    - we have placed timeouts in server sockets at both of these places, which ensure the reliability of the system.
    
    - Apart from the above changes, we have send ACKs after every chunk of file
    that is transferred. And as explained earlier, we used the same algorithm to
    mark the end of the file, by combination of specific ACKs, repeated sending and
    timeouts.

    Please Check the code to get more insight. 