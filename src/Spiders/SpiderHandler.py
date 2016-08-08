import SpiderLog
import threading
import SpiderQueue
import SpiderWorker
import Queue
import ClassesSpider

logger = SpiderLog.getLogger()

# list all type of url
CONST_ROOT_URL = 1
CONST_PACKAGE_LIST_URL = 2
CONST_PACKAGE_URL = 3
CONST_CLASS_LIST_URL = 4
CONST_CLASS_URL =5

class SpiderHandler(threading.Thread):
    def __init__(self, rootUrl):
        self.handlerMap = {}
        self.inQue = Queue.Queue()
        self.outQue = Queue.Queue()
        self.worker = SpiderWorker.WorkerCore(self.inQue, self.outQue)
        self.id = 1
        self.inQue.put(SpiderQueue.SpiderWorker(rootUrl, self.id))
        self.handlerMap[self.id] = CONST_ROOT_URL
        self.canRun = True

    def stop(self):
        self.outQue.join()
        self.canRun = False

    def doJob(self):
        if(self.outQue.qsize() > 0):
            ret = self.outQue.get()
            if ret.msg != "":
                if ret.id in self.handlerMap:
                    msgType = self.handlerMap[ret.id]
                    del self.handlerMap[ret.id]
                    switch msgType:
                        case CONST_ROOT_URL:
                            self.handleRootUrl(task.msg)
                            break
                        case CONST_PACKAGE_LIST_URL:
                            self.handlePackageListUrl(task.msg)
                            break
                        case CONST_PACKAGE_URL:
                            self.handlePackageUrl(task.msg)
                            break
                        case CONST_CLASS_LIST_URL:
                            self.handleClassListUrl(task.msg)
                            break
                        case CONST_CLASS_URL:
                            self.handleClassUrl(task.msg)
                            break
                        defautl:
                            #should be error!


    def handleClassUrl(self):
        pass

    def handleClassListUrl(self):
        pass

    def handlePackageUrl(self):
        pass

    def handlePackageListUrl(self):
        pass

    def handleRootUrl(self):
        pass

    def run(self):
        # now worker run
        self.worker.run()
        while self.canRun:
            self.doOneJob()
            logger.debug("handler heart beat")
