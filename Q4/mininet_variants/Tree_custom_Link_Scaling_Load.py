from time import sleep
from mininet.cli import CLI
from mininet.log import lg, info
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from functools import partial
from mininet.util import pmonitor


class TreeCustomTopo( Topo ):
    "Topology for a string of N hosts and N-1 switches."

    def build( self ):
        # Create switches and hosts
        hostName = ['S','H','I','J','K','L','M','N','O', 'S1', 'S2']
        hosts = []
        for h in hostName: 
            hosts.append(self.addHost( '%s' % h ))
        switchName = ['s1','s2','s3','s4','s5','s6','s7']
        switches = []
        for s in switchName:
            switches.append(self.addSwitch( '%s' % s ))

        # Wire up switches
        self.addLink(switches[0],switches[1], cls=TCLink , bw =400)
        self.addLink(switches[0],switches[2], cls=TCLink , bw =400)
        self.addLink(switches[1],switches[3], cls=TCLink , bw =200)
        self.addLink(switches[1],switches[4], cls=TCLink , bw =200)
        self.addLink(switches[2],switches[5], cls=TCLink , bw =200)
        self.addLink(switches[2],switches[6], cls=TCLink , bw =200)
        
        # Wire up hosts
        j = 3
        i = 1
        self.addLink( hosts[0], switches[0], cls=TCLink, bw = 400 )
        self.addLink( hosts[9], switches[5], cls=TCLink, bw = 400 )
        self.addLink( hosts[10], switches[6], cls=TCLink, bw = 400 )
        while(i<9):
            self.addLink(hosts[i],switches[j],cls=TCLink, bw = 100 )
            i+=1
            self.addLink(hosts[i],switches[j],cls=TCLink, bw = 100 )
            i+=1
            j+=1


def main():
    lg.setLogLevel( 'info')
    topo = TreeCustomTopo()
    net = Mininet(topo=topo)
    net.start()
    
    
    S = net.get('S')
    S1 = net.get('S1')
    S2 = net.get('S2')
    H = net.get('H')
    # I = net.get('I')
    # J = net.get('J')
    K = net.get('K')
    # L = net.get('L')
    M = net.get('M')
    N = net.get('N')
    # O = net.get('O')

    

    popens = {}
    p1 = S.popen('python3 ../tcp_thread/tcp_server.py %s & ' %S.IP())
    p2 = S1.popen('python3 ../tcp_thread/tcp_server.py %s & ' %S1.IP())
    p3 = S2.popen('python3 ../tcp_thread/tcp_server.py %s & ' %S2.IP())
    popens[S] = p1
    popens[S1] = p2
    popens[S2] = p3

    (H.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 1 %s |& tee -a output.log &' %S.IP()))
    # (I.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 2 %s |& tee -a output.log &' %S.IP()))
    # (J.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 3 %s |& tee -a output.log &' %S1.IP()))
    (K.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 2 %s |& tee -a output.log &' %S.IP()))
    #(L.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 2 %s |& tee -a output.log &' %S.IP()))
    (M.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 3 %s |& tee -a output.log &' %S1.IP()))
    (N.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 4 %s |& tee -a output.log &' %S2.IP()))
    #(O.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 4 %s |& tee -a output.log &' %S.IP()))

    # for host, line in pmonitor( popens ):
    #     if(host):
    #         info( "<%s>: %s" % ( host.name, line ) )
    
    sleep(5)
    S.cmd('chmod 777 output.log')
    with open('output.log', 'r') as fin:
        print(fin.read())
    
    S.cmd('sudo rm output.log')
    p1.terminate()
    p2.terminate()
    p3.terminate()
    net.stop()

if __name__ == '__main__':
    main()
    