import logging  
import logging.handlers  
import sys

handler = logging.StreamHandler(sys.stdout)
fmt = '%(asctime)s |%(filename)s:%(lineno)s |%(name)s :%(message)s'  
  
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
  
logger = logging.getLogger('Spider')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG) 

def getLogger():
    return logger

def setLoggerLevel(level):
    logger.setLoggerLevel(level)
