import unittest
import ClassesSpider

class TestStringMethods(unittest.TestCase):
    def test_whole(self):
      rootUrl = 'http://api.mongodb.com/java/current/'
      spider = ClassesSpider.Spider(rootUrl, "JavaMongo")
      spider.run()

if __name__ == '__main__':
    unittest.main()

