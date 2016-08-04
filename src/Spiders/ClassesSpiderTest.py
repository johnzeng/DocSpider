import unittest
import urllib2
import ClassesSpider
import sys,traceback
import logging  
import logging.handlers  
  
handler = logging.StreamHandler(sys.stdout)
fmt = '%(asctime)s |%(filename)s:%(lineno)s |%(name)s :%(message)s'  
  
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
  
logger = logging.getLogger('Tester')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)  
  

class PartsTester:
    def brufPull(self, url):
      #This is a tester, so should get error if any wrong is happen
      request = urllib2.Request(url)
      response = urllib2.urlopen(request)
      msg = response.read()
      return msg

    def RunTest(self, parts, version, url, testClassesList):
        logger.debug("now begin to do test for url:" + url)
        try:
            root = self.brufPull(url)
            versions = ClassesSpider.SpiderParts.versionReg.findall(root)
            #check version
            for v in versions:
                if -1 == v.find(version):
                    logger.error("can not find version")
                    return False
            #check package summary page 
            packagePage = self.brufPull(url + parts.PackageSummaryPage)
            #check package summary page re
            packages = parts.PackageRefRe.findall(packagePage)
            if len(packages) == 0:
                logger.error("can not find packages")
                return False
            for p in packages:
                logger.debug(p)
            #check classes page
            classesListPage = self.brufPull(url + parts.ClassesListPage)
            #check the classes re
            classes = parts.ClassesRefRe.findall(classesListPage)
            tcSet = set(testClassesList)

            methodFlag = False
            nestedClassFlag = True
            if len(classes) == 0:
                print classesListPage
                logger.error("can not get classes")
                return False
            for c in classes:
                logger.debug("get page:" + c[0])
                if c[0].replace(".html","").replace("/",".") in tcSet:
                    #only test the listed classes
                    logger.debug(url + c[0])
                    classPage = self.brufPull(url + c[0])
                    for s in parts.SummaryRe.findall(classPage):
                        for ss in parts.MemberSummaryRe.findall(s):
                            if ss[0].lower().find("nested") != -1:
                                nestedClassFlag = False
                                for nestedC in parts.SubClassRe.findall(ss[1]) :
                                    logger.debug("get nestedClass:" + nestedC[0])
                                    nestedClassFlag = True
                            else:
                                for methods in parts.MemberRefRe.findall(ss[1]):
                                    logger.debug("get method:" + methods[0])
                                    methodFlag = True
            return methodFlag and nestedClassFlag
        except:
            tb = traceback.format_exc()
            logger.error(tb)
            return False


class TestBeta(unittest.TestCase):
    def test_BetaParts(self,):
      parts = ClassesSpider.SpiderPartsBeta
      url = 'http://api.mongodb.com/java/2.0/'
      tester = PartsTester()
      ret = tester.RunTest(parts, "1.6.0", url, ['org.bson.BasicBSONCallback', 'com.mongodb.DB.WriteConcern', 'com.mongodb.MongoException'])
      self.assertTrue(ret)

class TestAlpha(unittest.TestCase):
    def test_AlphaParts(self,):
      parts = ClassesSpider.SpiderPartsAlpha
      url = 'http://api.mongodb.com/java/current/'
      tester = PartsTester()
      ret = tester.RunTest(parts, "1.8.0", url, ['org.bson.AbstractBsonReader', 'com.mongodb.WriteConcern'])
      self.assertTrue(ret)


if __name__ == '__main__':
    alphaSuite = unittest.TestLoader().loadTestsFromTestCase(TestAlpha)
    betaSuite = unittest.TestLoader().loadTestsFromTestCase(TestBeta)
    alltests = unittest.TestSuite([
        alphaSuite,
        betaSuite
        ])
    unittest.TextTestRunner(verbosity=2).run(alltests)

