'''
Description
'''

import sys, os, time, json, subprocess, traceback, random, string
from pythonLib import *
from engineChrome import timeout, TimeoutError

browserLoadTimeout = 3*60


def initialize():
    configs = Configs()

    configs.set('waitBetweenLoads'  , 2)
    configs.set('waitBetweenRounds' , 1)
    configs.set('rounds'            , 10)
    configs.set('pageLoadTimeout'   , 120)

    configs.set('closeDrivers'      , True)
    configs.set('clearCacheConns'   , True)

    configs.set('browserPath'       , False)

    configs.set('quicServerIP'      , "192.168.1.1")
    configs.set('quicServerPort'    , "6121")


    configs.set('httpsServerIP'     , "192.168.1.1")
    configs.set('httpsServerPort'     , "443")


    configs.set('cases'             , 'https,quic')

    configs.set('mainDir'           , os.path.abspath('../data') + '/results')

    configs.read_args(sys.argv)

    '''
    Important: the following MUST be done AFTER read_args in case "--against" gets overridden 
    '''
    if configs.get('against') == 'emulab':
        configs.set('host', {'quic'         :'www.example-quic.org',
                             'https'        :'www.example-tcp.org',})
        
    configs.check_for(['testDir', 'testPage'])
    
    if configs.get('testDir').endswith('/'):
        configs.set( 'testDir', configs.get('testDir')[:-1] )
    
    # configs.set('chromedriver', selectChromeDriverPath(configs.get('browserPath'), configs.get('platform')))
    
    configs.set('testDir', configs.get('mainDir') + '/' + configs.get('testDir') )
    
    if os.path.isdir(configs.get('testDir')):
        print('Test directory already exists! Use another name!')
        sys.exit()
    
    #Creating the necessary directory hierarchy
    PRINT_ACTION('Creating the necessary directory hierarchy', 0)        
    testDir         = configs.get('testDir')
    resultsDir      = '{}/resultsDir'.format(testDir)
    statsDir        = '{}/statsDir'.format(testDir)
    userDirs        = '{}/userDirs'.format(testDir)
    screenshotsDir  = '{}/screenshots'.format(testDir)
    dataPaths       = '{}/dataPaths'.format(testDir)
    netLogs         = '{}/netLogs'.format(testDir)
    tcpdumpDir      = '{}/tcpdumps'.format(testDir)
    tcpdumpFile     = '{}/{}_tcpdump.pcap'.format(testDir, os.path.basename(testDir))
    configsFile     = '{}/{}_configs.txt'.format(testDir, os.path.basename(testDir))
      
    os.system('mkdir -p {}'.format(resultsDir))
    os.system('mkdir -p {}'.format(statsDir))
    os.system('mkdir -p {}'.format(userDirs))
    os.system('mkdir -p {}'.format(screenshotsDir))
    os.system('mkdir -p {}'.format(dataPaths))
    os.system('mkdir -p {}'.format(netLogs))
    os.system('mkdir -p {}'.format(tcpdumpDir))
     
    #Write configs to file (just for later reference)
    configs.write2file(configsFile)
    
    cases         = configs.get('cases').split(',')
    methods       = {'quic'         :'https', 
                     'https'        :'https'}
    
    uniqeOptions  = {'quic' : [
                             '--enable-quic',
                             '--origin-to-force-quic-on={}:443'.format(configs.get('host')['quic']),
                             '--host-resolver-rules=MAP {}:443 {}:{}'.format(configs.get('host')['quic'], configs.get('quicServerIP'), configs.get('quicServerPort')),
                             '--ignore-certificate-errors-spki-list=a7+zGcPMs2Ws+y+LHm9Y1UUiXQNRoVjUcAcsu+7RLeI=',
                             ],
                    
                    'https': [
                             '--disable-quic',
                             '--host-resolver-rules=MAP {}:443 {}:{}'.format(configs.get('host')['https'], configs.get('httpsServerIP'), configs.get('httpsServerPort')),
                             '--ignore-certificate-errors-spki-list=5SqnBDsYKyH6GvRLlPRhOLXOeq0++PAtuMMSBYl3opI=',
                             ],               
                    }
    
    try:
        configs.get('quic-version')
        uniqeOptions['quic'].append( '--quic-version=QUIC_VERSION_{}'.format(configs.get('quic-version')) )
        uniqeOptions['quic-proxy'].append( '--quic-version=QUIC_VERSION_{}'.format(configs.get('quic-version')) )
        uniqeOptions['quic-proxy-mobile'].append( '--quic-version=QUIC_VERSION_{}'.format(configs.get('quic-version')) )
    except KeyError:
        pass
    
    
    dIPs = {'quic'          : configs.get('quicServerIP'),
            'https'         : configs.get('httpsServerIP'),
            }
    
    return configs, cases, methods, testDir, resultsDir, statsDir, userDirs, screenshotsDir, dataPaths, netLogs, tcpdumpDir, tcpdumpFile, uniqeOptions



class Driver(object):
    def __init__(self):
        self.process         = None
        self.pageLoadTimeout = str(Configs().get('pageLoadTimeout'))

    # Starts browser
    def open(self, browserPath, options, debugPort):
        self.randomID  = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))
        self.debugPort = debugPort
        cmd            = [browserPath] + options + ['--remote-debugging-port={}'.format(self.debugPort), '--randomID={}'.format(self.randomID)]
        self.process   = subprocess.Popen(cmd)
        time.sleep(3)
        
    # Closes browser    
    def close(self):
        '''
        This is a hack I came up with to close the browser. Everytime a browser window is opened, it's ran with a dummy "--randomID" switch.
        When closing, this function kills processes with this randomID in their name.
        '''
        os.system('sudo pkill -f {}'.format(self.randomID))
    
    # Request resource and capture timings using har-capturer
    @timeout(browserLoadTimeout)
    def get(self, url, outFile):
        cmd = ['chrome-har-capturer', '--force', '--give-up', self.pageLoadTimeout, '--port', self.debugPort, '-o', outFile, url]

        print(' '.join(cmd))
        self.process  = subprocess.Popen(cmd)
        self.process.communicate()

        try:
            with open(outFile, 'r') as f:
                j = json.load(f)
                print('\t\t', j['log']['pages'][0]['pageTimings']['onLoad'])
        except:
            pass

def main():
    #The following line is to make sure the script has sudo privilage to run tcpdump
    os.system('sudo echo')


    #Setting up configs
    PRINT_ACTION('Reading configs file and args', 0)
    configs, cases, methods, testDir, resultsDir, statsDir, userDirs, screenshotsDir, dataPaths, netLogs, tcpdumpDir, tcpdumpFile, uniqeOptions = initialize()
    configs.show_all()

    #Creating options
    '''
    IMPORTANT: --enable-benchmarking --enable-net-benchmarking: to enable the Javascript interface that allows chrome-har-capturer to flush the DNS cache and the socket pool before loading each URL.
               in other words, clear cache and close connections between runs! 
    '''
    PRINT_ACTION('Creating options', 0)
    drivers       = {}    
    # Stats module missing
    chromeOptions = {}
#     commonOptions = ['--no-first-run']
    commonOptions = [
                        '--no-sandbox',
                        '--headless',
                        '--disable-gpu',
                        '--no-first-run',
                        '--disable-background-networking', 
                        '--disable-client-side-phishing-detection', 
                        '--disable-component-update', 
                        '--disable-default-apps', 
                        '--disable-hang-monitor', 
                        '--disable-popup-blocking', 
                        '--disable-prompt-on-repost', 
                        '--disable-sync', 
                        '--disable-web-resources', 
                        '--metrics-recording-only', 
                        '--password-store=basic', 
                        '--safebrowsing-disable-auto-update', 
                        '--use-mock-keychain', 
                        '--ignore-certificate-errors'
                    ] 
    
    if configs.get('clearCacheConns'):
        commonOptions += ['--enable-benchmarking', '--enable-net-benchmarking']    

    debugPorts = {
                'https'       : '9221',
                'quic'        : '9222',
                }

    #Creating driver instances and modifying /etc/hosts
    PRINT_ACTION('Creating driver options and modifying /etc/hosts', 0)
    for case in cases:
        
        drivers[case] = Driver()
        
        chromeOptions[case] = []
        unCommonOptions     = ['--user-data-dir={}/{}'.format(userDirs, case),
                               '--data-path={}/{}'.format(dataPaths, case),
#                                '--log-net-log={}/{}.json'.format(netLogs, case),
                               ]
         
        chromeOptions[case] = uniqeOptions[case] + commonOptions + unCommonOptions
        
        if not configs.get('closeDrivers'):
            print('\tFor: {}...\t'.format(case), end=' '); sys.stdout.flush()
            drivers[case].open(configs.get('browserPath'), chromeOptions[case], debugPorts[case])
            print('Done')    
            
    # Starting TCPDUMP (Client side)


    # Asking remote host to start QUIC server

        # Asking remote host to start runTcpProbe

    
    # Generate side Traffic

    #Firing off the tests
    PRINT_ACTION('Firing off the tests', 0)
    for round in range(1, configs.get('rounds')+1):
        for case in cases:
            testID = '{}_{}'.format(case, round)
            PRINT_ACTION('Doing: {}/{}'.format(testID, configs.get('rounds')), 1, action=False)            
            
            url = '{}://{}/{}'.format(methods[case], configs.get('host')[case], configs.get('testPage'), testID)            

            # Do stats
            # Do TCP dump    


            if configs.get('closeDrivers'):
                PRINT_ACTION('Opening driver: '+ testID, 2, action=False)
                drivers[case].open(configs.get('browserPath'), chromeOptions[case], debugPorts[case])
            try:
                drivers[case].get(url, resultsDir + '/' + testID + '.har')
            except TimeoutError:
                    print('Browser load timeout ({}) happend!!!'.format(browserLoadTimeout))
                    os.system('sudo pkill -f chrome-har-capturer')
                    time.sleep(5)
            except Exception as e:
                print('###### EXCEPTION during {}#######'.format(testID))
                print(e)
                traceback.print_exc()
                continue
            
            if configs.get('closeDrivers'):
                PRINT_ACTION('Closing drivers', 0)
                drivers[case].close()
             
            time.sleep(configs.get('waitBetweenLoads'))

        if round != configs.get('rounds'):
            PRINT_ACTION('Sleeping between rounds: {} seconds ...'.format(configs.get('waitBetweenRounds')), 0)
            time.sleep(configs.get('waitBetweenRounds'))
            
    PRINT_ACTION('Running final beforeExit ...', 0)

    #Closing drivers
    if drivers:
        PRINT_ACTION('Closing drivers', 0)
        for case in drivers:
            try:
                drivers[case].close()
            except TimeoutError:
                print('Got stuck closing drivers! :-s')
    
    time.sleep(3)

if __name__=="__main__":
    main()    