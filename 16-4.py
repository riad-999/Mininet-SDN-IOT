import os
import sys
from time import sleep
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

    sensor1 = net.addSensor('sensor1', ip='2003::1/64',position='20,90,0')
    sensor2 = net.addSensor('sensor2', ip='2003::2/64',position='24,80,0')
    sensor3 = net.addSensor('sensor3', ip='2003::3/64',position='28,80,0')
    sensor4 = net.addSensor('sensor4', ip='2003::4/64',position='32,80,0')
    switch1 = net.addSwitch('switch1')

    sensor5 = net.addSensor('sensor5', ip='2003::5/64',position='58,90,0')
    sensor6 = net.addSensor('sensor6', ip='2003::6/64',position='60,60,0')
    sensor7 = net.addSensor('sensor7', ip='2003::7/64',position='62,60,0')
    sensor8 = net.addSensor('sensor8', ip='2003::8/64',position='66,60,0')
    switch2 = net.addSwitch('switch2')

    sensor9 = net.addSensor('sensor9', ip='2003::9/64',position='36,120,0')
    sensor10 = net.addSensor('sensor10', ip='2003::10/64',position='38,150,0')
    sensor11 = net.addSensor('sensor11', ip='2003::11/64',position='41,150,0')
    sensor12 = net.addSensor('sensor12', ip='2003::12/64',position='45,150,0')
    switch3 = net.addSwitch('switch3')

    sensor13 = net.addSensor('sensor13', ip='2003::13/64',position='60,120,0')
    sensor14 = net.addSensor('sensor14', ip='2003::14/64',position='55,150,0')
    sensor15 = net.addSensor('sensor15', ip='2003::15/64',position='60,150,0')
    sensor16 = net.addSensor('sensor16', ip='2003::16/64',position='65,150,0')
    switch4 = net.addSwitch('switch4')

    c1 = net.addController('c1')

    info("*** Configuring nodes\n")
    net.configureWifiNodes()

    info("*** Associating Nodes\n")

    net.addLink(sensor1,cls=SixLowpan,panid='pan1')
    net.addLink(sensor1,switch1)
    net.addLink(sensor2,cls=SixLowpan,panid='pan1')
    net.addLink(sensor3,cls=SixLowpan,panid='pan1')
    net.addLink(sensor4,cls=SixLowpan,panid='pan1')

    net.addLink(sensor5,cls=SixLowpan,panid='pan2')
    net.addLink(sensor5,switch2)
    net.addLink(sensor6,cls=SixLowpan,panid='pan2')
    net.addLink(sensor7,cls=SixLowpan,panid='pan2')
    net.addLink(sensor8,cls=SixLowpan,panid='pan2')

    net.addLink(sensor9,cls=SixLowpan,panid='pan3')
    net.addLink(sensor9,switch3)
    net.addLink(sensor10,cls=SixLowpan,panid='pan3')
    net.addLink(sensor11,cls=SixLowpan,panid='pan3')
    net.addLink(sensor12,cls=SixLowpan,panid='pan3')

    net.addLink(sensor13,cls=SixLowpan,panid='pan4')
    net.addLink(sensor13,switch4)
    net.addLink(sensor14,cls=SixLowpan,panid='pan4')
    net.addLink(sensor15,cls=SixLowpan,panid='pan4')
    net.addLink(sensor16,cls=SixLowpan,panid='pan4')


    net.addLink(switch1,switch2)
    net.addLink(switch2,switch3)
    net.addLink(switch3,switch4)

    server = net.addHost('server')
    net.addLink(server,switch1)

    info("*** Starting network\n")
    net.build()
    c1.start()
    switch1.start([c1])
    switch2.start([c1])
    switch3.start([c1])
    switch4.start([c1])
    

    # emptying file
    os.system("echo '' > result-udp.txt")

    sensor1.cmd('ip -6 addr add 2003::71/64 dev sensor1-eth1')
    sensor5.cmd('ip -6 addr add 2003::76/64 dev sensor5-eth1')
    sensor9.cmd('ip -6 addr add 2003::81/64 dev sensor9-eth1')
    sensor13.cmd('ip -6 addr add 2003::86/64 dev sensor13-eth1')
    server.cmd('ip -6 addr add 2003::100/64 dev server-eth0')

    sensor1.cmd("ping -I sensor1-eth1 -c2 2003::100")
    sensor5.cmd("ping -I sensor5-eth1 -c2 2003::100")
    sensor9.cmd("ping -I sensor9-eth1 -c2 2003::100")
    sensor13.cmd("ping -I sensor13-eth1 -c2 2003::100")

    #---------------------------------------------------------------
    sleep(2)
    #servers
    info("*** staring servers \n")
    revcievers = [sensor1,sensor5,sensor9,sensor13]
    for revciever in revcievers:
        revciever.cmd('iperf -V -s -u -p 4444 -t 30 >> result-udp.txt &')
    # sensor1.cmd('iperf -V -s -u -p 4444 -t 30 >> result-udp.txt &')
    # sensor5.cmd('iperf -V -s -u -p 4444 -t 30 >> result-udp.txt &')
    # sensor9.cmd('iperf -V -s -u -p 4444 -t 30 >> result-udp.txt &')
    # sensor13.cmd('iperf -V -s -u -p 4444 -t 30 >> result-udp.txt &')
    #clients
    sensor2.cmd('iperf -V -u -c 2003::1 -p 4444 -b 120Kb &')
    sensor3.cmd('iperf -V -u -c 2003::1 -p 4444 -b 120Kb &')
    sensor4.cmd('iperf -V -u -c 2003::1 -p 4444 -b 120Kb &')

    sensor6.cmd('iperf -V -u -c 2003::5 -p 4444 -b 120Kb &')
    sensor7.cmd('iperf -V -u -c 2003::5 -p 4444 -b 120Kb &')
    sensor8.cmd('iperf -V -u -c 2003::5 -p 4444 -b 120Kb &')

    sensor10.cmd('iperf -V -u -c 2003::9 -p 4444 -b 120Kb &')
    sensor11.cmd('iperf -V -u -c 2003::9 -p 4444 -b 120Kb &')
    sensor12.cmd('iperf -V -u -c 2003::9 -p 4444 -b 120Kb &')

    sensor14.cmd('iperf -V -u -c 2003::13 -p 4444 -b 120Kb &')
    sensor15.cmd('iperf -V -u -c 2003::13 -p 4444 -b 120Kb &')
    sensor16.cmd('iperf -V -u -c 2003::13 -p 4444 -b 120Kb &')

    info("*** staring CLI")
    CLI_wifi(net)
    

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    mob = True if '-m' in sys.argv else False
    topology()