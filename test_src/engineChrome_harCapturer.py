'''
Description
'''

import sys, os, time, json, subprocess, traceback, random, string
from pythonLib import *
from engineChrome import initialize, timeout, TimeoutError

# This might timeout for large file (10mb) [default: 3*60, extreme: 100*60]
browserLoadTimeout = 3*60

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
                               '--log-net-log={}/{}.json'.format(netLogs, case),
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
