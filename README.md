# DocSpider
A spider to grab document from web and build an index for Dash to read it.If you want to build your own doc reader, you can get the index file and search it by yourself.

##How to use:
Currently, you can just run the script by calling 

``` python
python src/main.py [root page] [docset name]
```

, the `root page` should be the summary of the java doc set, for example, `http://api.mongodb.com/java/current/` this is the summary page of MongoDB API. `[docset name]` can be any name that you want. It will generate a file named `[docset name].docset`, import it into Dash, and you can then enjoy it.

## what to do if you want to add a new spider:
Create a new spider parts, and provide the following regular mathin fields like the alpha and beta spider:

```python
class SpiderPartsAlpha:
    #this spider is created for 1.8.0_xx javadoc set, I beleive they should be same so far
        #provide the allclasses page, please use the noframe page
    ClassesListPage = 'allclasses-noframe.html'
    #provide the package page, please use the no frame page
    PackageSummaryPage = 'overview-summary.html'
    #pravide the re to grab the package link , in tuple (link, package name)
    PackageRefRe = re.compile('<td class="colFirst"><a href="(.*?)">(.*?)</a></td>')
    #pravide the re to grab the classes link in a class list page, in tuple (link, class type)
    ClassesRefRe = re.compile('<li><a href="(.*)".*?title="(.*?) in .*?"')
    #pravide the re to grab the css file, other wise you will get a ugly page
    CsRefRe = re.compile('href="(\..*?\.css)"')
    #pravide the re to grab the methods in a class page, in tuple(link, method name)
    MemberRefRe = re.compile('<span class="memberNameLink"><a href="(.*?html#.*?)">(.*?)</a></span>')
    #pravide the re to grab the class in a class page, in tuple(link, class type)
    SubClassRe = re.compile('<span class="memberNameLink"><a href="(.*?)" title="(.*?) in')
    #pravide the re to grab the whole summary table in a class page (including the method summary, constructor summary, field summary, sub class summary)
    SummaryRe = re.compile('<div class="summary">(.*?)<div class="details">', re.S)
    #pravide the re to grab the sub summary table in a class page (please spilt the xx summary into different matching)
    MemberSummaryRe = re.compile('<a name="(.*?)">(.*?)</ul>', re.S)
    
```

If your matching is the same as some of the existing parts, you can use it like the beta parts:

``` python
class SpiderPartsBeta(SpiderPartsAlpha):
```
 
##supported doc
Java doc:1.8.0_xx
Java doc:1.6.0_xx

##known limitation
- Just grab the package summary pages , method pages, all classes page, all package page. Thus you will find some link unavailable but it shouldn't be a problem.
- Don't grab images, I don't sure if these are important, I may grab it in the future.
- This project is using only one thread to do everything, so it's a little slow and I don't wanna do multi-threading on this project recently.


