from Spiders import ClassesSpider

import sys, getopt

if __name__ == "__main__":
#  I don't sure if we will need these codes or not so I just leavel it here
#  opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
#  input_file=""
#  output_file=""
#  for op, value in opts:
#    if op == "-i":
#      input_file = value
#    elif op == "-o":
#      output_file = value
#    elif op == "-h":
#      print "don't show help msg :)"
#      sys.exit()
#    elif op == "":
#      print value
  rootUrl = sys.argv[-2]
  docName = sys.argv[-1]
  spider = ClassesSpider.Spider(rootUrl, docName)
  spider.run()
