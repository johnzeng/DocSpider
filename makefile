
test:
	- rm -rf JavaMongo.docset/
	python ./src/main.py 'http://api.mongodb.com/java/current/' 'JavaMongo'
