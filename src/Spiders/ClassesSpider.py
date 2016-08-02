# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import os
import urlparse
import sys,traceback
import sqlite3
import plistlib

class SpiderPartsAlpha:
  #this spider is created for 1.8.0_xx javadoc set, I beleive they should be same so far
  ClassesListPage = 'allclasses-noframe.html'
  PackageSummaryPage = 'overview-summary.html'
  PackageRefRe = re.compile('<td class="colFirst"><a href="(.*?)">(.*?)</a></td>')
  ClassesRefRe = re.compile('<li><a href="(.*)".*?title="(.*?) in .*?"')
  CsRefRe = re.compile('href="(\..*?\.css)"')
  MemberRefRe = re.compile('<span class="memberNameLink"><a href="(.*?html#.*?)">(.*?)</a></span>')
  SummaryRe = re.compile('<div class="summary">(.*?)<div class="details">', re.S)
  MemberSummaryRe = re.compile('<a name="(.*?)">(.*?)</ul>', re.S)

class SpiderParts:
  VersionMap = {
          "1.8.0" :SpiderPartsAlpha
          }
  versionReg = re.compile('<!-- Generated by javadoc \((.*?)\)')

  @staticmethod
  def getSpider(root):
    #find the doc version
    try:
      request = urllib2.Request(root )
      response = urllib2.urlopen(request)
      msg = response.read()
      versionMatch = SpiderParts.versionReg.findall(msg)
      for version in versionMatch:
        print "The doc version is " + version
        for key, value in SpiderParts.VersionMap.items():
          if version.find(key) != -1:
            print "match spider found"
            return value
      return None
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
        return None
    

class IndexDataBase:
  def __init__(self, docSetName):
    self.connection = sqlite3.connect('./%s.docset/Contents/Resources/docSet.dsidx' % docSetName)
    self.course = self.connection.cursor()
    self.course.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
    self.course.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')
    self.insertStr = '''INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?, ?, ?);'''

  def __del__(self):
    self.connection.commit()
    self.connection.close()

  def commit(self):
    self.connection.commit()

  def insert(self, name, type, path):
    self.course.execute(self.insertStr, (name, type, path))

#This is the base Spider, you should only use this spider
class Spider:
  ##const parameters
  dirPathRe = re.compile('(.*)/')
  docSetNameReg = re.compile('(.*)\.html')

  def __init__(self,root, docSetName):
    self.createPath('./%s.docset/Contents/Resources/Documents/test.txt' % docSetName)
    self.rootUrl = root
    self.parts = SpiderParts.getSpider(root)
#don't sure about index page, are they the same?
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    self.headers = { 'User-Agent' : user_agent }
    self.searchedUrl = set()
    self.docSetName = docSetName
    self.initPlist()
    self.tagDic = {
        'annotation':'Annotation',
        'nested.class':'Class',
        'class':'Class',
        'interface':'Interface',
        'enum':'Enum',
        'enum.constant':'Enum',
        'method':'Method',
        'constructor':'Constructor',
        'field':'Constant'
       }
    self.db = IndexDataBase(docSetName)

  def pullWeb(self, url):
    try:
      if url in self.searchedUrl:
        return ""
      request = urllib2.Request(url,headers = self.headers)
      response = urllib2.urlopen(request)
      rspMsg = response.read()
      self.searchedUrl.add(url)
      return rspMsg
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
        return ""

  def pullSummaryPage(self):
    summaryPage = self.rootUrl + self.parts.PackageSummaryPage
    summaryPageMsg = self.pullWeb(summaryPage)
    self.write2File(summaryPageMsg, summaryPage)
    packageRe = self.parts.PackageRefRe
    allPackages = packageRe.findall(summaryPageMsg)
    for package in allPackages:
        packageRequest = urlparse.urljoin(summaryPage, package[0])
        packageMsg = self.pullWeb(packageRequest)
        packagePath = self.write2File(packageMsg, packageRequest)
        name = self.getClassName(packagePath)
        self.db.insert(name[0], "Package", packagePath)



  def initPlist(self):
    plistInfo = {
        "CFBundleIdentifier": "javadoc",
        "CFBundleName" : self.docSetName,
        "DocSetPlatformFamily": "javadoc",
        "dashIndexFilePath" : "overview-summary.html",
        "DashDocSetFamily" :"java",
        "isDashDocset": "YES"
        }
    fileName = './%s.docset/Contents/Info.plist' %self.docSetName
    self.createPath(fileName)
    plistlib.writePlist(plistInfo, fileName)


  def createPath(self,file):
    docPath = Spider.dirPathRe.findall(file)
    for p in docPath:
      if os.path.exists(p) is not True :
          os.makedirs(p)
      return p
    return ""

  def write2File(self, msg, url):
    print "now save %s" % url
    fileName = url.replace(self.rootUrl, "./%s.docset/Contents/Resources/Documents/" % self.docSetName)
    path = self.createPath(fileName)
    fileHandler = open(fileName,'w')
    fileHandler.write(msg)
    return fileName.replace("./%s.docset/Contents/Resources/Documents/" % self.docSetName,"")

  def getClassName(self, url):
    allClass = Spider.docSetNameReg.findall(url)
    for path in allClass:
      splited = path.split('/')
      return ".".join(splited), splited[-1]
    return "", ""


  def getTypeName(self, javaTag):
    if javaTag in self.tagDic:
      return self.tagDic[javaTag]
    else:
      print "unexpected tag:%s"%javaTag
      return javaTag[0].capitalize() + javaTag[:1]
    
  def run(self):
    try:
        allClassUrl = self.rootUrl + self.parts.ClassesListPage
        rspMsg = self.pullWeb(allClassUrl)
        # also save method list
        self.write2File(rspMsg, allClassUrl)

        # I don't care if this is a doc or not, just get the first one, if nothing exist, panic will rasie    
        #find the classes and interfaces, also find the href
#        self.pullSummaryPage()

        classReg = self.parts.ClassesRefRe
        allClass = classReg.findall(rspMsg)

        csPathRe = self.parts.CsRefRe
        allSummaryStrReg = self.parts.SummaryRe
        allSummaryReg = self.parts.MemberSummaryRe
        pageReg = self.parts.MemberRefRe

        for cur in allClass:
          self.db.commit()
          requestUrl = self.rootUrl + cur[0]
          classMsg = self.pullWeb(requestUrl)
          #save classes
          fileName = self.write2File(classMsg, requestUrl)
          classNameA, classNameB = self.getClassName(fileName)

          typeName = self.getTypeName(cur[1])
          self.db.insert(classNameA, typeName, fileName)
          self.db.insert(classNameB, typeName, fileName)

          #find all method in this file and insert into the db
          methodSummaryStr = allSummaryStrReg.findall(classMsg)
          for str in methodSummaryStr:
            methodSummary = allSummaryReg.findall(str)
            for method in methodSummary:
              #find field summary at first
              if -1 == method[0].find(".summary"):
                # if no summary is found, than this could be something like "method.inherited from xxx", so we just continue it
                continue
              memberFields = pageReg.findall(method[1])

              fieldType = self.getTypeName(method[0].replace(".summary",""))
              for field in memberFields:
                methodIndex = urlparse.urljoin(fileName, field[0])
                self.db.insert(field[1], fieldType, methodIndex)
            csFile = csPathRe.findall(classMsg)
            for files in csFile:
              downloadPath = urlparse.urljoin(self.rootUrl + cur[0],  files)
              cssFile = self.pullWeb(downloadPath)
              if cssFile != "":
                self.write2File(cssFile, downloadPath)
    except:
        tb = traceback.format_exc()
        print(tb)

