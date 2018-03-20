# Ethereum-Contract-Web3

## Installation Dependencies
```
python 3.5
	http://ubuntuhandbook.org/index.php/2017/07/install-python-3-6-1-in-ubuntu-16-04-lts/

sudo apt-get install python3.5-dev

easy_install3
	sudo apt install python3-setuptools
	sudo easy_install3 pip

sudo add-apt-repository ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install solc

sudo pip3 install web3
pip install py-solc
```

## Framework
  - Blockchain System : Ethereum (solidity)
  - Backend : Web3 (Python3.5+)
  - API : Restful (Java servlet)
  - Web : Javascript

## Compile API
```
# chahge python path in java code
$ javac -cp /opt/tomcat/apache-tomcat-7.0.72/lib/servlet-api.jar:/tmp/json.jar CheckContract.java # compile three java code~
$ mv CheckContract.class /opt/tomcat/apache-tomcat-7.0.72/webapps/ROOT/WEB-INF/classes/ # move three java class to tomcat path
$ sudo /opt/tomcat/apache-tomcat-7.0.72/bin/shutdown.sh
$ sudo /opt/tomcat/apache-tomcat-7.0.72/bin/startup.sh
```

## Docker
```
# 啟動 Docker

$ sed -i 's/localhost/REAL_IP/g' /opt/tomcat/webapp/blockVote/index.js
$ ipfs daemon &
$ sudo /opt/tomcat/bin/startup.sh

第1台：
	$ echo '{ "Data": "Vote" }' | ipfs object put
	$ ipfs pin add QmWvMxzFoKjUh4nF9Knf5XSYguVgzArzVZcsNXUJComLvD
	$ python3 Application/deploy...
```
