from time import sleep
from mininet.cli import CLI
from mininet.log import lg, info
from mininet.topo import SingleSwitchTopo
from mininet.net import Mininet
from mininet.util import pmonitor

def main():
    lg.setLogLevel( 'info')
    topo = SingleSwitchTopo(6)

    net = Mininet(topo=topo)

    net.start()

    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')
    h5 = net.get('h5')
    h6 = net.get('h6')
    popens = {}
    p1 = h1.popen('python3 ../tcp_thread/tcp_server.py %s & ' %h1.IP())
    popens[h1] = p1

    print(h2.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 1 %s |& tee -a output.log &' %h1.IP()))
    print(h3.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 1 %s |& tee -a output.log &' %h1.IP()))
    print(h4.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 1 %s |& tee -a output.log &' %h1.IP()))
    print(h5.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 1 %s |& tee -a output.log &' %h1.IP()))
    print(h6.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 1 %s |& tee -a output.log &' %h1.IP()))

    for host, line in pmonitor( popens ):
        if(host):
            info( "<%s>: %s" % ( host.name, line ) )
    # CLI(net)
    p1.terminate()
    sleep(1)
    h6.cmd('chmod 777 output.log')
    with open('output.log', 'r') as fin:
        print(fin.read())
    
    h6.cmd('sudo rm output.log')
    net.stop()

if __name__ == '__main__':
    main()