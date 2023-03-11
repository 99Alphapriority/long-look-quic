'''
Description
'''

try:
    from selenium import webdriver
except ImportError:
    print('\n####################################################################')
    print('SELENIUM NOT AVAILABLE!!! You can only run tests using HAR capturer!!!')
    print('####################################################################\n')
# import sys, os, time, pickle, socket, json, subprocess, traceback, multiprocessing, subprocess
# import stats
# import sideTrafficGenerator
# from pythonLib import *
# from functools import wraps
# import errno
# import os
# import signal


class Driver(object):
    def __init__(self, chromeDriverPath, browserPath, options, pageLoadTimeOut=None):
        self.chromeDriverPath = chromeDriverPath
        self.browserPath      = browserPath
        self.options          = options
        self.pageLoadTimeOut  = pageLoadTimeOut
        self.driver           = None    

    # @timeout(20)
    def open(self):
        webdriver.ChromeOptions.binary_location = self.browserPath
        
        self.driver = webdriver.Chrome(executable_path=self.chromeDriverPath, chrome_options=self.options)
        
        if self.pageLoadTimeOut:
            self.driver.set_page_load_timeout(self.pageLoadTimeOut)

    # @timeout(20)
    def close(self):
        self.driver.close()
        self.driver.quit()
        
    def get(self, url):
        self.driver.get(url)

    def clearCacheAndConnections(self):
        self.driver.execute_script("return chrome.benchmarking.clearCache();")
        self.driver.execute_script("return chrome.benchmarking.clearHostResolverCache();")
        self.driver.execute_script("return chrome.benchmarking.clearPredictorCache();")
        self.driver.execute_script("return chrome.benchmarking.closeConnections();")


def main():

    # create chrome driver options
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--headless")


    # creating driver instances
    driver = Driver("/proj/FEC-HTTP/long-quic/chromedriver_linux64/chromedriver", "/proj/FEC-HTTP/long-quic/chromium/src/out/Default/chrome", chromeOptions)

    driver.open()

    driver.get("https://www.python.org")
    print(driver.driver.title)

if __name__=="__main__":
    main()