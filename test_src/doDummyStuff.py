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

    # Performa Jitter locally on link_bridge 
    # to achieve high frequency change in latency 
    def addJitter(self, bw, baseDelayDown, varDelayDown, baseDelayUp, varDelayUp, interval=0.1):
        counter     = 0
        prevDelayDown = -1
        prevDelayUp   = -1

        print("baseDelayDown, varDelayDown, baseDelayUp, varDelayUp")
        print(baseDelayDown, varDelayDown, baseDelayUp, varDelayUp)

        while True:
            # build command
            dummyCmd1 = 'sudo ipfw pipe {} config '.format(self.pipe1)
            dummyCmd2 = 'sudo ipfw pipe {} config '.format(self.pipe2)
        
            if bw:
                dummyCmd1 += 'bw {}Mbit/s '.format(bw)
                dummyCmd2 += 'bw {}Mbit/s '.format(bw)

            counter += 1
            if baseDelayDown == 0:
                delayDown = 0
            else:
                delayDown = random.randrange(baseDelayDown-varDelayDown, baseDelayDown+varDelayDown)
            if baseDelayUp == 0:
                delayUp = 0
            else:
                delayUp   = random.randrange(baseDelayUp-varDelayUp, baseDelayUp+varDelayUp)

            if (delayDown < prevDelayDown) or (delayUp < prevDelayUp):
                steps = 2
                gapDown = prevDelayDown - delayDown
                gapUp   = prevDelayUp   - delayUp
            
                for i in range(1, steps+1):
                    tmpDelayDown = prevDelayDown - i*gapDown/steps
                    tmpDelayUp   = prevDelayUp - i*gapUp/steps

                    # Add tmpDelayDown , tmpDelayUp
                    # print("Adding Delay T: ", tmpDelayDown," ",tmpDelayUp)
                    if tmpDelayUp+tmpDelayDown:
                        dummyCmd1 += 'delay  {}ms '.format(tmpDelayUp)
                        dummyCmd2 += 'delay  {}ms '.format(tmpDelayDown)
                    
                    os.system("{} && {}".format(dummyCmd1, dummyCmd2))
                    time.sleep(interval/steps)
            else:
                # Add delay delayDown, delayUp
                # print("Adding Delay : ", delayDown," ", delayUp)
                if delayUp+ delayDown:
                    dummyCmd1 += 'delay  {}ms '.format(delayUp)
                    dummyCmd2 += 'delay  {}ms '.format(delayDown)

                os.system("{} && {}".format(dummyCmd1, dummyCmd2))
                time.sleep(interval)

            prevDelayDown = delayDown
            prevDelayUp   = delayUp         


def main():
    
    # Call main function to do jitter direclty on link bridge
    project = "FEC-HTTP"
    experiment = "Q043"
    bw = 100
    link = DummyNet(project, experiment, "link_bridge")
    # build jitter process
    pJitter = multiprocessing.Process(target=link.addJitter, args=(bw,50, 5, 50, 5))

    print("Bandwidth : ", bw )
    # start jitter
    print("Starting Jitter")
    pJitter.start()

    # Wait for 100 sec
    # time.sleep(30)
    
    signal = input("enter stop:")

    if signal == "stop":
        # Stop Jitter
        print("Ending Jitter")
        pJitter.terminate()
    
    # pass    

if __name__ == '__main__':
    main()