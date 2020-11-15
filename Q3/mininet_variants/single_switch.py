from time import sleep
from mininet.cli import CLI
from mininet.log import lg, info
from mininet.topo import SingleSwitchTopo
from mininet.net import Mininet

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

    p1 = h1.popen('python3 ../tcp_thread/tcp_server.py %s & ' %h1.IP())

    print(h2.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 1 %s' %h1.IP()))
    print(h3.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 1 %s' %h1.IP()))
    print(h4.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 1 %s' %h1.IP()))
    print(h5.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 1 %s' %h1.IP()))
    print(h6.cmd('python3 ../tcp_thread/tcp_client_non_persistent.py 1 %s' %h1.IP()))

    CLI(net)
    p1.terminate()
    net.stop()

if __name__ == '__main__':
    main()