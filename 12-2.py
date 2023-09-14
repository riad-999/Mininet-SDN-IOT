import os
import sys

from mininet.log import setLogLevel, info
from mn_iot.mac80211.cli import CLI_wifi
from mininet.node import RemoteController
from mn_iot.mac80211.net import Mininet_wifi
from mn_iot.mac802154.link import SixLowpan


IP = '172.17.0.5'
PORT = 6653


def topology():
    "Create a network."
    net = Mininet_wifi(controller=lambda name: RemoteController(name,ip=IP,port=PORT)) 

    info("*** Creating nodes\n")
    #group1
    sensor1 = net.addSensor('sensor1', ip='2003::1/64',position='25,90,0')
    sensor2 = net.addSensor('sensor2', ip='2003::2/64',position='20,80,0')
    sensor3 = net.addSensor('sensor3', ip='2003::3/64',position='30,80,0')
    sensor4 = net.addSensor('sensor4', ip='2003::4/64',position='20,70,0')
    sensor5 = net.addSensor('sensor5', ip='2003::5/64',position='25,70,0')
    sensor6 = net.addSensor('sensor6', ip='2003::6/64',position='30,70,0')
    ap1 = net.addAccessPoint('ap1', panid='pan1',range=200,position='25,100,0')
    #group1
    sensor7 = net.addSensor('sensor7', ip='2003::7/64',position='85,90,0')
    sensor8 = net.addSensor('sensor8', ip='2003::8/64',position='80,80,0')
    sensor9 = net.addSensor('sensor9', ip='2003::9/64',position='90,80,0')
    sensor10 = net.addSensor('sensor10', ip='2003::10/64',position='95,90,0')
    sensor11 = net.addSensor('sensor11', ip='2003::11/64',position='100,90,0')
    sensor12 = net.addSensor('sensor12', ip='2003::12/64',position='105,90,0')
    ap2 = net.addAccessPoint('ap2', panid='pan2',range=200,position='82,100,0')

    #adding a controller
    c1 = net.addController('c1')

    info("*** Configuring nodes\n")
    net.configureWifiNodes()

    info("*** Associating Nodes\n")
    #creating links
    #group1
    # edge sendor
    net.addLink(sensor1,cls=SixLowpan,panid='pan1')
    net.addLink(sensor1,ap1)
    net.addLink(sensor2,cls=SixLowpan,panid='pan1')
    net.addLink(sensor3,cls=SixLowpan,panid='pan1')
    net.addLink(sensor4,cls=SixLowpan,panid='pan1')
    net.addLink(sensor5,cls=SixLowpan,panid='pan1')
    net.addLink(sensor6,cls=SixLowpan,panid='pan1')
    #group1
    # edge sendor
    net.addLink(sensor7,cls=SixLowpan,panid='pan2')
    net.addLink(sensor7,ap2)
    net.addLink(sensor8,cls=SixLowpan,panid='pan2')
    net.addLink(sensor9,cls=SixLowpan,panid='pan2')
    net.addLink(sensor10,cls=SixLowpan,panid='pan2')
    net.addLink(sensor11,cls=SixLowpan,panid='pan2')
    net.addLink(sensor12,cls=SixLowpan,panid='pan2')

    #server
    server = net.addHost('server')
    net.addLink(ap1,server)
    #associating switches
    net.addLink(ap1,ap2)

    
    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    
    #configuring nodes interfaces
    sensor1.cmd('ip -6 addr add 2003::71/64 dev sensor1-eth1')
    sensor7.cmd('ip -6 addr add 2003::77/64 dev sensor7-eth1')
    server.cmd('ip -6 addr add 2003::100/64 dev server-eth0')
    #ping
    sensor1.cmd("ping -I sensor1-eth1 -c2 2003::100")
    sensor7.cmd("ping -I sensor7-eth1 -c2 2003::100")

    # emptying file
    os.system("echo '' > result-udp.txt")
    
    info("*** staring recievers \n")
    sensor1.cmd('iperf -V -s -u -p 4444 -t 40 >> result-udp.txt &')
    sensor2.cmd('iperf -V -s -u -p 4444 -t 40 >> result-udp.txt &')
    sensor3.cmd('iperf -V -s -u -p 4444 -t 40 >> result-udp.txt &')

    sensor7.cmd('iperf -V -s -u -p 4444 -t 40 >> result-udp.txt &')
    sensor8.cmd('iperf -V -s -u -p 4444 -t 40 >> result-udp.txt &')
    sensor9.cmd('iperf -V -s -u -p 4444 -t 40 >> result-udp.txt &')

    info("*** connecting and sending to revcievers")
    sensor3.cmd('iperf -V -u -c 2003::1 -p 4444 -b 120Kb &')
    sensor2.cmd('iperf -V -u -c 2003::1 -p 4444 -b 120Kb &')
    sensor4.cmd('iperf -V -u -c 2003::2 -p 4444 -b 120Kb &')
    sensor5.cmd('iperf -V -u -c 2003::2 -p 4444 -b 120Kb &')
    sensor6.cmd('iperf -V -u -c 2003::3 -p 4444 -b 120Kb &')

    sensor8.cmd('iperf -V -u -c 2003::7 -p 4444 -b 120Kb &')
    sensor9.cmd('iperf -V -u -c 2003::7 -p 4444 -b 120Kb &')
    sensor10.cmd('iperf -V -u -c 2003::8 -p 4444 -b 120Kb &')
    sensor11.cmd('iperf -V -u -c 2003::8 -p 4444 -b 120Kb &')
    sensor12.cmd('iperf -V -u -c 2003::9 -p 4444 -b 120Kb &')

    info("*** staring CLI")
    CLI_wifi(net)
    
    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    mob = True if '-m' in sys.argv else False
    topology()