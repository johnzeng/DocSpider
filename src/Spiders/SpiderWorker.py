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
    class PoorWorker(threading.Thread):
        def __init__(self,task,oq):
            self.task = task
            self.que = oq

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
        def run(self):
            msg = pullWeb(self.task.url)
            if "" != msg:
                # I don't know if I should write it like this or not..
                outTask = {
                        msg:msg,
                        qid:task.qid
                        }
                self.oq.put(outTask)

            
    def __init__(self,iq,oq):
        threading.Thread.__init__(self)
        self.canRun = True
        self.running = False
        self.que = iq
        self.out = oq

    def stop(self):
        # should wait until all jobs are done
        self.que.join()
        self.canRun = False

    def pullOneJobFromQueue(self):
        if(self.que.qsize() > 0):
            task = self.que.get()
            print task
            self.que.task_done()
        
    def run(self):
        while self.canRun:
            self.pullOneJobFromQueue()
            #sleep 0.1s so you won't use too much net work
            time.sleep(1)
            logger.debug("worker heart beat")


