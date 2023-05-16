'''
Script modified to work for dummynet commands
'''

import sys, os, random, time, multiprocessing, subprocess
from pythonLib import *

class DummyNet(object):
    def __init__(self, projectName, experimentName, nodeName, pipe1='60111', pipe2='60121'):
        self.projectName = projectName
        self.experimentName = experimentName
        self.nodeName = nodeName
        self.pipe1 = pipe1
        self.pipe2 = pipe2 
        self.pipes = [pipe1, pipe2]
        self.sshNode = "ssh {}.{}.{}.emulab.net ".format(nodeName, experimentName, projectName)

    def show(self):
        print('Dummynet on {}:'.format("Link Bridge"))
        os.system("{} 'sudo ipfw pipe show'".format(self.sshNode))

    def remove(self):
        # Remove shaping
        print("Removing traffic shaping...")
        for p in self.pipes:
            # Remove Bandwidth
            os.system("{} 'sudo ipfw pipe {} config bw  0Mbit/s delay  0ms plr  0'".format(self.sshNode,p))


    def add(self, bw, delay, plr):
        dummyCmd1 = 'sudo ipfw pipe {} config '.format(self.pipe1)
        dummyCmd2 = 'sudo ipfw pipe {} config '.format(self.pipe2)

        if bw:
            dummyCmd1 += 'bw {}Mbit/s '.format(bw)
            dummyCmd2 += 'bw {}Mbit/s '.format(bw)

        if delay:
            dummyCmd1 += 'delay  {}ms '.format(delay)
            dummyCmd2 += 'delay  {}ms '.format(delay)
        
        if plr:
            dummyCmd1 += 'plr {} '.format(plr)
            dummyCmd2 += 'plr {} '.format(plr)

        print("Add traffic shaping")
        os.system("{} {}".format(self.sshNode, dummyCmd1))
        os.system("{} {}".format(self.sshNode, dummyCmd2))

 
def main():
    pass    

if __name__ == '__main__':
    main()