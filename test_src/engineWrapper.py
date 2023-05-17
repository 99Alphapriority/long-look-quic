'''

'''

import sys, os, multiprocessing
from pythonLib import *
from doDummyStuff import DummyNet

obj_set1  = [ '5k.html', '10k.html', '100k.html', '200k.html', '500k.html', '1mb.html', '10mb.html',]  
obj_set2  = [ '1mbx1.html','500kx2.html' ,'200kx5.html' ,'100kx10.html', '10kx100.html', '5kx200.html' ]  

ratesX = "10_36_0,50_36_0,100_36_0,10_112_0,50_112_0,100_112_0,10_36_1,50_36_1,100_36_1"
indexX = "5k,10k,100k,200k,500k,1mb,10mb,1mbx1,500kx2,200kx5,100kx10,10kx100,5kx200"

# Configs for running experiments , 
# different from configs controlling chrome options, servers etc
def initialize():
    configs = Configs()

    configs.set('project', 'FEC-HTTP')
    configs.set('experiment', 'Q043')

    configs.set('pythonBinary', '/proj/FEC-HTTP/nenv/bin/python')
    configs.set('mainDir', '')

    configs.set('rates'             ,  "10_36_0,50_36_0,100_36_0,10_112_0,50_112_0,100_112_0,10_36_1,50_36_1,100_36_1")
    # configs.set('qualities'         , 'hd2160,hd1440,hd1080,hd720,large,medium,small,tiny,auto')
    configs.set('stopTime'          , '60')
    configs.set('indexes'           , "5k,10k,100k,200k,500k,1mb,10mb,1mbx1,500kx2,200kx5,100kx10,10kx100,5kx200")
    configs.set('networkInt'        , 'eth0')
    configs.set('rounds'            , 20)
    configs.set('tcpdump'           , False)
    configs.set('doSideTraffic'     , False)
    configs.set('runQUICserver'     , False)
    configs.set('runTcpProbe'       , False)
    configs.set('doJitter'          , False)
    configs.set('doIperf'           , True)
    configs.set('doPing'            , True)
    configs.set('closeDrivers'      , False)
    configs.set('clearCacheConns'   , True)
    configs.set('separateTCPDUMPs'  , False)
    configs.set('browserPath'       , False)
    configs.set('addPeakRate'       , False)
    configs.set('lossArgs'          , False)
    configs.set('delayArgs'         , False)
    configs.set('changeBW'          , False)
    configs.set('latencyOrLimit'    , 'latency')
    configs.set('against'           , 'emulab')
    configs.set('quic_server_path'  , '')
    configs.set('script2run'        , 'engineChrome_harCapturer.py')
    
    configs.read_args(sys.argv)
    configs.show_all()

    return configs


def run(configs, link):

    for rate in configs.get('rates').split(','):

        bw = int(rate.split('_')[0])
        delay = int(rate.split('_')[1])
        plr = int(rate.split('_')[2])

        print("Bandwidth :", bw)
        print("Delay :", delay)
        print("Loss :", plr)

        # Do traffic shaping
        link.show()

        link.add(bw, (delay/2), (plr/100))

        link.show()

        # Create Directory
        dirName = rate
        print('Creating directory')
        os.system('mkdir -p {}/{}'.format(configs.get('mainDir'), dirName))

        # Run network tests
        if configs.get('doIperf'):
            print('Running iperf ...')
            if configs.get('against') == 'emulab':
                # iperfServer = "[iPerf should be running on the same host as QUIC/HTTPS server]"
                iperfServer = "192.168.1.1"
            print('./do_iperf.sh {}/{}/ {}'.format(configs.get('mainDir'), dirName, iperfServer))
            os.system('./do_iperf.sh {}/{}/ {}'.format(configs.get('mainDir'), dirName, iperfServer))
        
        if configs.get('doPing'):
            print('Running pings ...')
            if configs.get('against') == 'emulab':
                # pingServer = "[QUIC/HTTPS server host address]"
                pingServer = "192.168.1.1"
            print('./do_ping.sh {}/{}/ {}'.format(configs.get('mainDir') , dirName, pingServer))
            os.system('./do_ping.sh {}/{}/ {}'.format(configs.get('mainDir'), dirName, pingServer))

        # Run benchmark scripts
        for index in configs.get('indexes').split(','):
            cmd  = '{} {} '.format(configs.get('pythonBinary'), configs.get('script2run'))
            cmd += '--against={} --networkInt={} '.format(configs.get('against'), configs.get('networkInt'))
            cmd += '--browserPath={} --quic-version={} '.format(configs.get('browserPath'), configs.get('quic-version') )
            cmd += '--mainDir={} '.format(configs.get('mainDir'))
            cmd += '--testDir={}/{}_html --testPage={}.html '.format(dirName, index, index)
            cmd += '--rounds={} '.format(configs.get('rounds'))
            print('\tThe command:\n\t', cmd)
            os.system(cmd)

        link.remove()
        print()        

def main():
    PRINT_ACTION('Reading configs file and args', 0)
    configs = initialize()
    link = DummyNet(configs.get('project'), configs.get('experiment'), "link_bridge")

    PRINT_ACTION('Running...', 0)
    run(configs, link)
    
if __name__ == "__main__":
    main()