from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest, time, re
import datetime
import multiprocessing
import threading

# modified by Xiaochen
# input: list file of (lat)

class ProcManager(object):
    def __init__(self):
        self.procs = []
        self.errors_flag = False
        self._threads = []
        self._lock = threading.Lock()

    def terminate_all(self):
        with self._lock:
            for p in self.procs:
                if p.is_alive():
                    print "Terminating %s" % p
                    p.terminate()

    def launch_proc(self, func, args=(), kwargs= {}):
        t = threading.Thread(target=self._proc_thread_runner,
                             args=(func, args, kwargs))
        self._threads.append(t)
        t.start()

    def _proc_thread_runner(self, func, args, kwargs):
        p = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
        self.procs.append(p)
        p.start()
        while p.exitcode is None:
            p.join()
        if p.exitcode > 0:
            self.errors_flag = True
            self.terminate_all()

    def wait(self):
        for t in self._threads:
            t.join()

def testworker_simpleload(weburl):   
    driver = webdriver.Firefox()
    while True:
        try:
            driver.get(weburl)
            time.sleep(0.2)
            #driver.close()
        except (KeyboardInterrupt, SystemExit):
            #driver.close()
            #driver.quit()
            raise Exception("keyboard captured")
        except:
            raise Exception("something wrong")
    #print "[GoodWorker] Starting"
    #time.sleep(4)
    #print "[GoodWorker] all good"

def bad_worker():
    print "[BadWorker] Starting"
    time.sleep(2)
    raise Exception("ups!")

def simpletest():
    driver = webdriver.Firefox()
    for i in range(5):
        driver.get("http://www.python.org")
        assert "Python" in driver.title
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

def GetLatLon():
    driver = webdriver.Firefox()
    for loc in xrange(10):
		driver.get('file:///home/xcliu/Downloads/gsv/streetview-events.html?lat=34.025540&&lng=-118.291565')
		# 34.0254404, -118.29159529999998
		table = driver.find_element_by_xpath('//td[@id="position-cell"]')
		table_html = table.get_attribute('innerHTML')
		#df = read_html(table_html)[0]
		#print df
		print table_html
		print datetime.datetime.now()
    driver.close()

if __name__ == '__main__':
	# add code here...
    GetLatLon()
