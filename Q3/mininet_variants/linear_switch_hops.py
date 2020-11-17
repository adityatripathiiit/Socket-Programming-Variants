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
                  for h in range( 1, 3 ) ]
        switches = [ self.addSwitch( 's%s' % s )
                     for s in range( 1, N+1) ]

        # Wire up switches
        last = None
        for switch in switches:
            if last:
                self.addLink( last, switch )
            last = switch

        # Wire up hosts
        self.addLink( hosts[0], switches[0] )
        self.addLink( hosts[1], switches[N-1])


def main(hop):
    lg.setLogLevel( 'info')
    topo = LinearTestTopo(hop)
    link = partial( TCLink, bw=1000)
    net = Mininet(topo=topo,link=link)
    net.start()

    h1 = net.get('h1')
    h2 = net.get('h2')

    p1 = h1.popen('python3 ../tcp_thread/tcp_server.py %s & ' %h1.IP())
    print("Starting transfer for hop: ",hop)

    print(h2.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 5 %s' %h1.IP()))


    # CLI(net)
    p1.terminate()
    net.stop()

if __name__ == '__main__':
    hops = [2,4,6,8,10]
    for hop in hops:
        main(hop)
    