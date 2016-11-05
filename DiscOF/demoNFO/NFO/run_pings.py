
from mininet.net import Mininet
from mininet.topolib import TreeTopo


from mininet.node import Node

from mininet.log import setLogLevel
import sys




from select import poll, POLLIN
from mininet.topo import *
from mininet.node import Controller, OVSSwitch,RemoteController
from mininet.cli import CLI


from time import time,sleep
import os,csv
import random
import RocketFuelMININERtopo,RocketfuelBigtopo,MininetTree 
import numpy as np

random.seed(448)


def startpings(ip_list,hosts_dict):
    "Tell host to repeatedly ping targets"

    #threading.Timer(pingsrechangeperiod, startpings,[ip_list,hosts]).start()
    print "#############################################"
    with open(os.getcwd() + '/' + "FinalResults/" + filename) as f:
        lines = f.readlines()
        
        for line in lines:
            dict = eval(line.strip('\n'))
            
            for hostip in dict:
                host = hosts_dict[hostip]   
                for targetip in dict[hostip]:
                    
                    host.cmd('   `ping -c %d %s | grep packets` &' % (dict[hostip][targetip],targetip))
                
                    print ( '*** Host %s (%s) will be pinging ips: %s' %
                            ( host.name, host.IP(), targetip ) )
            sleep(pingsrechangeperiod)

    #for host in hosts:
        #host.cmd( 'kill %while' )


def multiping():
    "Select topology type:"
    


    #tree4 = TreeTopo(depth=2,fanout=10)
    #t=RocketFuelMININERtopo.SampleTopo()
    #t=RocketfuelBigtopo.SampleTopo()
    #t=MininetTree.SampleTopo()

    
    __import__(networkidentifier)
    t= eval(networkidentifier).SampleTopo()
    net = Mininet(topo=t, controller=lambda a: RemoteController(a, defaultIP='127.0.0.1', port=6633))
    net.start()
    
    
    switches = net.switches
    hosts = net.hosts
    numofswitches=len(switches)
    numofhosts = len(hosts)
    

    #net.pingAll()
          


    with open(os.getcwd() + '/' + "FinalResults/networkTopo.csv", 'w') as outcsv:   
    #configure writer to write standard csv file
        writer = csv.writer(outcsv, delimiter=',',quoting=csv.QUOTE_MINIMAL)
        writer.writerow([numofswitches,numofhosts,networkidentifier,initialFlowEntries,pingsrechangeperiod,lamda,beta])


    #net.pingAll()
    
    for l in range (1,numofswitches+1):
        os.system("sudo ovs-vsctl add bridge  " +  "s" + format(l) + "  flow_tables 0=@nam1 -- --id=@nam1 \
        create flow_table flow_limit=" + format(initialFlowEntries))

    ip_list = [ host.IP() for host in hosts]
    
    
    hosts_dict = {}
    sig=open(os.getcwd() + '/' + "mininet_signal.txt","w")
    sig.close()    
    for host in hosts:
        hosts_dict[host.IP()] = host
        
    
    if not os.path.isfile(os.getcwd() + '/' + "FinalResults/" + filename):
        
        
      for _ in range(totalduration):
          dict = {}
          for host in hosts:
            dict[host.IP()] ={}
            targets = random.sample(ip_list,np.random.poisson(lamda, None)) #lamda =7
            
            for targetip in targets:
                
                if(targetip != host.IP()):
                    
                    duration = random.expovariate(beta)#beta =0.01
                    dict[host.IP()][targetip] = duration
          
          f = open(os.getcwd() + '/' + "FinalResults/" + filename,'a')
          
          f.write(str(dict) + '\n')
           
          f.close()
    

            
                    
                
                
#     endTime = time() + totalduration
#     
#     while time() < endTime:
#     
#         startpings(ip_list,hosts)
# 
#         sleep(pingsrechangeperiod)  #sleep period
    startpings(ip_list,hosts_dict)
    net.stop()
    

    
if __name__ == '__main__':

    column =int(sys.argv[1])
    with open(os.getcwd() + '/' + 'MininetInputsFile.csv') as file:
        line = list(file)[column].strip('\n')
        args=line.split(',')
        print args
       
    setLogLevel( 'info' )


    initialFlowEntries = int(args[0])
    totalduration = int(args[1])
    networkidentifier = str(args[2])
    lamda = float(args[3])
    beta = float(args[4])
    pingsrechangeperiod = int(args[5])
    filename = str(args[6]).strip()

    multiping()

