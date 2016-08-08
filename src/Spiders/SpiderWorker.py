import SpiderLog
import urllib2
import threading
import time 

logger = SpiderLog.getLogger()


searchedUrl = []
searchedUrlLock = threading.Lock()
def addSearchedUrl(url):
    searchedUrlLock.acquire(True)
    searchedUrl.add(url)
    searchedUrlLock.release()

class WorkerCore(threading.Thread):

    def pullWeb(self, url):
        try:
            if url in searchedUrl:
              return ""
            addSearchedUrl(url)
            request = urllib2.Request(url,)
            response = urllib2.urlopen(request)
            rspMsg = response.read()
            return rspMsg
        except urllib2.URLError, e:
            if hasattr(e,"code"):
                logger.error(e.code)
            if hasattr(e,"reason"):
                logger.error(e.reason)
            logger.error("request:%s" % url)
            return ""
            
    def __init__(self,iq,oq):
        threading.Thread.__init__(self)
        self.canRun = True
        self.inQue = iq
        self.outQue = oq

    def stop(self):
        # should wait until all jobs are done
        self.inQue.join()
        self.canRun = False

    def pullOneJobFromQueue(self):
        if(self.inQue.qsize() > 0):
            task = self.inQue.get()
            msg = pullWeb(task.msg)
            if msg != "":
                task.msg = msg
                self.outQue.put(task)
            self.inQue.task_done()
        
    def run(self):
        while self.canRun:
            self.pullOneJobFromQueue()
            #sleep 0.1s so you won't use too much net work
            time.sleep(0.1)
            logger.debug("worker heart beat")


