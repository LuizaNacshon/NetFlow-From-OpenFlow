"""Custom topology script for Mininet
 
Creates custom tree with parameters depth and fanout (count of childs per parent node)
Use: mn --custom %PATH to script%/%script_name%.py --topo custom
 
"""
 
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
import itertools
 
class SampleTopo(Topo):
       
    # fanout - number of child switch per parent switch"
   
    def __init__(self, depth=2, fanout=3, **opts):#10
        # Initialize topology and default options
        Topo.__init__(self, **opts)
       
        #core_switch = self.addSwitch('c1')
        switches = {} #map {depth_level : [list of nodes]}
        hosts = []
        parend_id = 0
        switches[0] = list()
        switch_id=1
        switches[0].append(self.addSwitch('s%s'%(switch_id)))
 
        for s in range(1, depth): #last is host level
            switches[s] = list() #initialize list for dict
            for sw in range(0,fanout**s):
                #print "switch_id = fanout**s+sw",sw+2
                switch_id = sw+2
                switches[s].append(self.addSwitch('s%s'%(switch_id)))
                self.addLink(switches[s][-1],switches[s-1][sw//fanout])
        fourfirstbits=[]
        for x in map(''.join, itertools.product('01', repeat=8)):
            fourfirstbits.append(x)
        j=0
        prev=0
        i=1
        for h in range(0, fanout**depth):
            #print "h//fanout)",(h//fanout),switches[depth-1][h//fanout]
            if(prev!=(h//fanout)):
                j=j+1
                i=1
                prev=(h//fanout)
            fourflastbits=[]
            for x1 in map(''.join, itertools.product('01', repeat=8)):
                fourflastbits.append(x1)
            #print "!!!",format(fourfirstbits[j]), format(fourflastbits[i])
            #hosts.append(self.addHost('h%s'%(h+1),ip='10.0.0.'+format(int(format(fourfirstbits[j])+ format(fourflastbits[i]),2))))
            hosts.append(self.addHost('h%s' % (h+1),ip='10.0.'+format(int(format(fourfirstbits[j]),2))+ '.' + format(int(format(fourflastbits[i]),2))))
            self.addLink(hosts[-1],switches[depth-1][h//fanout])
            i=i+1
            
 
 

                   
topos = { 'customtree': ( lambda: SampleTopo(depth=2,fanout=10) ) }  # set params here
