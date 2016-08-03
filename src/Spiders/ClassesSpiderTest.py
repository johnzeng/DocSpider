import unittest
import ClassesSpider
import sys,traceback

class PartsTester:
    def brufPull(self, url):
      #This is a tester, so should get error if any wrong is happen
      request = urllib2.Request(root )
      response = urllib2.urlopen(request)
      msg = response.read()
      return msg

    def RunTest(self, parts, version, url, testClassesList):
        try:
            root = self.brufPull(url)
            versions = ClassesSpider.SpiderParts.versionReg.findall(root)
            #check version
            for v in versions:
                if -1 == v.find(version):
                    return False
            #check package summary page 
            packagePage = self.brufPull(url + parts.PackageSummaryPage)
            #check package summary page re
            packages = parts.PackageRefRe.findall(packagePage)
            if len(packages) == 0:
                return False
            #check classes page
            classesListPage = self.brufPull(url + parts.ClassesListPage)
            #check the classes re
            classes = parts.ClassesRefRe.findall(classesListPage)
            tcSet = set(testClassesList)

            methodFlag = False
            nestedClassFlag = True
            for c in classes:
                if c[0].replace(".html","").replace("/",".") in tcSet:
                    #only test the listed classes
                    classPage = self.brufPull(root + c[0])
                    for s in parts.SummaryRe(classPage):
                        for ss in parts.MemberSummaryRe(s):
                            if ss[0].find("nested") != -1:
                                nestedClassFlag = False
                                for nestedC in parts.SubClassRe.findall(ss[1]) :
                                    nestedClassFlag = True
                            else
                                for methods in parts.MemberRefRe.findall(ss[1]):
                                    methodFlag = True
            return methodFlag and nestedClassFlag


            


        except:
            tb = traceback.format_exc()
            print(tb)
            return False


class TestStringMethods(unittest.TestCase):
    def test_whole(self):
      rootUrl = 'http://api.mongodb.com/java/current/'
      spider = ClassesSpider.Spider(rootUrl, "JavaMongo")
      try:
          spider.run()
        except:
            tb = traceback.format_exc()
            print(tb)


    def test_AlphaParts(self):
      parts = ClassesSpider.SpiderPartsAlpha
      url = 'http://api.mongodb.com/java/current/'
      tester = PartsTester()
      tester.RunTest(parts, "1.8.0", url)

if __name__ == '__main__':
    unittest.main()

