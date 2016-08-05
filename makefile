
test:
	export PYTHONPATH="./src/Spiders/"&& python `find ./testc/ -name *Test.py`

dev:
	- rm -rf Mongo2.docset
	- rm -rf Mongo3.docset
	python ./src/main.py http://api.mongodb.com/java/2.0/overview-summary.html Mongo2
	python ./src/main.py http://api.mongodb.com/java/current/ Mongo3
