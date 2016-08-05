import SpiderLog
import SpiderWorker
import unittest
import Queue

logger = SpiderLog.getLogger()

class TestWorker(unittest.TestCase):
    def test_workerQue(self,):
        logger.debug("test worker")
        q = Queue.Queue()
        worker = SpiderWorker.WorkerCore(q)
        worker.start()
        q.put("hello")
        q.put("hi")
        worker.stop()

if __name__ == "__main__":
    unittest.main()
