from time import sleep
from mininet.cli import CLI
from mininet.log import lg, info
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from functools import partial


class LinearTestTopo( Topo ):
    "Topology for a string of N hosts and N-1 switches."

    def build( self, N, **params ):
        # Create switches and hosts
        hosts = [ self.addHost( 'h%s' % h )
                  for h in range( 1, N+1 ) ]
        switches = [ self.addSwitch( 's%s' % s )
                     for s in range( 1, N) ]

        # Wire up switches
        last = None
        for switch in switches:
            if last:
                self.addLink( last, switch )
            last = switch

        # Wire up hosts
        self.addLink( hosts[ 0 ], switches[ 0 ] )
        for host, switch in zip( hosts[ 1: ], switches ):
            self.addLink( host, switch )


def main(bandwidth):
    lg.setLogLevel( 'info')
    topo = LinearTestTopo(2)                                                          # Creating a custom linear topology as required
    link = partial( TCLink, bw=bandwidth)                                             # Setting the bandwidth of the link       
    net = Mininet(topo=topo, link=link)                                               # Creating the network
    net.start()                                                                       # Starting the network 

    h1 = net.get('h1')                                                                # Getting host h1
    h2 = net.get('h2')                                                                # Getting host h2
 
    p1 = h1.popen('python3 ../tcp_thread/tcp_server.py %s & ' %h1.IP())               # Starting the server 
    print("Starting transfer for bandwidth: ", bandwidth)                               

    print(h2.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 5 %s' %h1.IP())) # starting the client

 
    p1.terminate()                                                                    # Terminating the server
    net.stop()                                                                        # Stopping the network

if __name__ == '__main__':
    #10 Mbps, 100 Mbps, 1000Mbps bandwidths respectively for each iteration 
    bandwidths = [10,100,1000]  
    for bandwidth in bandwidths:
        main(bandwidth)
    