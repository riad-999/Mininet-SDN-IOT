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

    sensor1 = net.addSensor('sensor1', ip='2003::1/64',position='28,110,0')
    sensor2 = net.addSensor('sensor2', ip='2003::2/64',position='20,90,0')
    sensor3 = net.addSensor('sensor3', ip='2003::3/64',position='30,90,0')
    sensor4 = net.addSensor('sensor4', ip='2003::4/64',position='35,90,0')
    sensor5 = net.addSensor('sensor5', ip='2003::5/64',position='35,70,0')
    sensor6 = net.addSensor('sensor6', ip='2003::6/64',position='40,70,0')
    sensor7 = net.addSensor('sensor7', ip='2003::7/64',position='25,70,0')
    sensor8 = net.addSensor('sensor8', ip='2003::8/64',position='20,70,0')
    # switch1 = net.addSwitch('switch1')
    ap1 = net.addAccessPoint('ap1', panid='pan1',range=200,position='28,120,0')

    sensor9 = net.addSensor('sensor9', ip='2003::9/64',position='88,110,0')
    sensor10 = net.addSensor('sensor10', ip='2003::10/64',position='80,90,0')
    sensor11 = net.addSensor('sensor11', ip='2003::11/64',position='90,90,0')
    sensor12 = net.addSensor('sensor12', ip='2003::12/64',position='95,90,0')
    sensor13 = net.addSensor('sensor13', ip='2003::13/64',position='95,70,0')
    sensor14 = net.addSensor('sensor14', ip='2003::14/64',position='100,70,0')
    sensor15 = net.addSensor('sensor15', ip='2003::15/64',position='85,70,0')
    sensor16 = net.addSensor('sensor16', ip='2003::16/64',position='80,70,0')
    ap2 = net.addAccessPoint('ap2', panid='pan2',range=200,position='80,120,0')
    
    sensor17 = net.addSensor('sensor17', ip='2003::17/64',position='55,20,0')
    sensor18 = net.addSensor('sensor18', ip='2003::18/64',position='50,40,0')
    sensor19 = net.addSensor('sensor19', ip='2003::19/64',position='55,40,0')
    sensor20 = net.addSensor('sensor20', ip='2003::20/64',position='60,40,0')
    sensor21 = net.addSensor('sensor21', ip='2003::21/64',position='60,60,0')
    sensor22 = net.addSensor('sensor22', ip='2003::22/64',position='65,60,0')
    sensor23 = net.addSensor('sensor23', ip='2003::23/64',position='55,60,0')
    sensor24 = net.addSensor('sensor24', ip='2003::24/64',position='50,60,0')
    ap3 = net.addAccessPoint('ap3', panid='pan3',range=200,position='60,10,0')

    c1 = net.addController('c1')

    info("*** Configuring nodes\n")
    net.configureWifiNodes()

    info("*** Associating Nodes\n")

    sensors = [sensor1,sensor2,sensor3,sensor4,sensor5,sensor6,sensor7,sensor8]
    for sensor in sensors:
        net.addLink(sensor,cls=SixLowpan,panid='pan1')
    net.addLink(sensor1,ap1)

    sensors = [sensor9,sensor10,sensor11,sensor12,sensor13,sensor14,sensor15,sensor16]
    for sensor in sensors:
        net.addLink(sensor,cls=SixLowpan,panid='pan2')
    net.addLink(sensor9,ap2)

    sensors = [sensor17,sensor18,sensor19,sensor20,sensor21,sensor22,sensor23,sensor24]
    for sensor in sensors:
        net.addLink(sensor,cls=SixLowpan,panid='pan3')
    net.addLink(sensor17,ap3)

    net.addLink(ap1,ap2)
    net.addLink(ap2,ap3)

    server = net.addHost('server')
    net.addLink(server,ap1)

    net.plotGraph(max_x=300, max_y=200)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])

    sensor1.cmd('ip -6 addr add 2003::71/64 dev sensor1-eth1')
    sensor9.cmd('ip -6 addr add 2003::79/64 dev sensor9-eth1')
    sensor17.cmd('ip -6 addr add 2003::87/64 dev sensor17-eth1')
    server.cmd('ip -6 addr add 2003::100/64 dev server-eth0')

    sensor1.cmd("ping -I sensor1-eth1 -c2 2003::100")
    sensor9.cmd("ping -I sensor9-eth1 -c2 2003::100")
    sensor17.cmd("ping -I sensor17-eth1 -c2 2003::100")

    # emptying file
    os.system("echo '' > result-udp.txt")
    
    #servers
    sensor1.cmd('iperf -V -s -u -t 40 -p 4444 >> result-udp.txt &')
    sensor2.cmd('iperf -V -s -u -t 40 -p 4444 >> result-udp.txt &')
    sensor3.cmd('iperf -V -s -u -t 40 -p 4444 >> result-udp.txt &')
    sensor4.cmd('iperf -V -s -u -t 40 -p 4444 >> result-udp.txt &')

    sensor9.cmd('iperf -V -s -u -t 40 -p 4444 >> result-udp.txt &')
    sensor10.cmd('iperf -V -s -u -t 40 -p 4444 >> result-udp.txt &')
    sensor11.cmd('iperf -V -s -u -t 40 -p 4444 >> result-udp.txt &')
    sensor12.cmd('iperf -V -s -u -t 40 -p 4444 >> result-udp.txt &')

    sensor17.cmd('iperf -V -s -u -t 40 -p 4444 >> result-udp.txt &')
    sensor18.cmd('iperf -V -s -u -t 40 -p 4444 >> result-udp.txt &')
    sensor19.cmd('iperf -V -s -u -t 40 -p 4444 >> result-udp.txt &')
    sensor20.cmd('iperf -V -s -u -t 40 -p 4444 >> result-udp.txt &')
    #clients
    sensor2.cmd('iperf -V -u -c 2003::1 -p 4444 -b 120Kb &')
    sensor3.cmd('iperf -V -u -c 2003::1 -p 4444 -b 120Kb &')
    sensor4.cmd('iperf -V -u -c 2003::1 -p 4444 -b 120Kb &')
    sensor5.cmd('iperf -V -u -c 2003::2 -p 4444 -b 120Kb &')
    sensor6.cmd('iperf -V -u -c 2003::2 -p 4444 -b 120Kb &')
    sensor7.cmd('iperf -V -u -c 2003::3 -p 4444 -b 120Kb &')
    sensor8.cmd('iperf -V -u -c 2003::4 -p 4444 -b 120Kb &')

    sensor10.cmd('iperf -V -u -c 2003::9 -p 4444 -b 120Kb &')
    sensor11.cmd('iperf -V -u -c 2003::9 -p 4444 -b 120Kb &')
    sensor12.cmd('iperf -V -u -c 2003::9 -p 4444 -b 120Kb &')
    sensor13.cmd('iperf -V -u -c 2003::11 -p 4444 -b 120Kb &')
    sensor14.cmd('iperf -V -u -c 2003::10 -p 4444 -b 120Kb &')
    sensor15.cmd('iperf -V -u -c 2003::11 -p 4444 -b 120Kb &')
    sensor16.cmd('iperf -V -u -c 2003::12 -p 4444 -b 120Kb &')

    sensor18.cmd('iperf -V -u -c 2003::17 -p 4444 -b 120Kb &')
    sensor19.cmd('iperf -V -u -c 2003::17 -p 4444 -b 120Kb &')
    sensor20.cmd('iperf -V -u -c 2003::17 -p 4444 -b 120Kb &')
    sensor21.cmd('iperf -V -u -c 2003::18 -p 4444 -b 120Kb &')
    sensor22.cmd('iperf -V -u -c 2003::18 -p 4444 -b 120Kb &')
    sensor23.cmd('iperf -V -u -c 2003::20 -p 4444 -b 120Kb &')
    sensor24.cmd('iperf -V -u -c 2003::19 -p 4444 -b 120Kb &')

    info("*** staring CLI")
    CLI_wifi(net)
    

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    mob = True if '-m' in sys.argv else False
    topology()