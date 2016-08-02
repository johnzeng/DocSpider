# DocSpider
A spider to grab document from web and build an index for Dash to read it.If you want to build your own doc reader, you can get the index file and search it by yourself.

##How to use:
Currently, you can just run the script by calling 

``` python
python src/main.py [root page] [docset name]
```

, the `root page` should be the summary of the java doc set, for example, `http://api.mongodb.com/java/current/` this is the summary page of MongoDB API. `[docset name]` can be any name that you want. It will generate a file named `[docset name].docset`, import it into Dash, and you can then enjoy it.
 
##supported doc
Java doc:1.8.0_66


##known limitation
- Just grab the package summary pages , method pages, all classes page, all package page. Thus you will find some link unavailable but it shouldn't be a problem.

