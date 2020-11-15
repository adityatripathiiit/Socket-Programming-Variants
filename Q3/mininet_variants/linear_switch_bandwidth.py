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
    topo = LinearTestTopo(2)
    link = partial( TCLink, bw=bandwidth)
    net = Mininet(topo=topo, link=link)
    net.start()

    h1 = net.get('h1')
    h2 = net.get('h2')

    p1 = h1.popen('python3 ../tcp_thread/tcp_server.py %s & ' %h1.IP())
    print("Starting transfer for bandwidth: ", bandwidth)

    print(h2.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 5 %s' %h1.IP()))


    # CLI(net)
    p1.terminate()
    net.stop()

if __name__ == '__main__':
    bandwidths = [10,100,1000]
    for bandwidth in bandwidths:
        main(bandwidth)
    