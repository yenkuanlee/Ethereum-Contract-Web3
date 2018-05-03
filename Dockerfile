# iServStor
FROM ubuntu:16.04
MAINTAINER Docker Newbee yenkuanlee@gmail.com

RUN apt-get -qq update

# Basic tool
RUN apt-get -qqy install sudo
RUN apt-get -qqy install python python-dev
RUN apt-get -qqy install wget
RUN apt-get -qqy install vim
RUN apt-get -qqy install sqlite3
RUN apt-get -qqy install net-tools # ifconfig
RUN apt-get -qqy install python-pkg-resources # iservstor need it, only for ubuntu 14.04

# update java
RUN apt-get -qq update
RUN apt-get -qqy install software-properties-common
RUN add-apt-repository -y ppa:webupd8team/java
RUN apt-get -qqy install openjdk-8-jdk

# for iota
RUN apt-get -qqy install git
RUN apt-get -qqy install python-setuptools
RUN apt-get -qqy install build-essential
RUN easy_install pip

#RUN apt-get -qqy install maven # long time ...
RUN apt-get -qq update

# for mcu
RUN apt-get -qqy install python3.5-dev
RUN apt -qqy install python3-setuptools
RUN easy_install3 pip
RUN add-apt-repository ppa:ethereum/ethereum
RUN apt-get update
RUN apt-get -qqy install solc
RUN pip3 install -Iv web3==3.16.5
RUN pip install py-solc
RUN apt-get install -y locales
RUN locale-gen zh_TW zh_TW.UTF-8 zh_CN.UTF-8 en_US.UTF-8
RUN echo 'export LC_ALL=zh_TW.utf8' >> /root/.bashrc

# tomcat
RUN cd /opt && wget http://www-us.apache.org/dist/tomcat/tomcat-7/v7.0.86/bin/apache-tomcat-7.0.86.tar.gz && tar xzf apache-tomcat-7.0.86.tar.gz&& mv apache-tomcat-7.0.86 tomcat7 && echo 'export CATALINA_HOME="/opt/tomcat7"' >> ~/.bashrc

# Add localadmin user
RUN useradd -m localadmin && echo "localadmin:openstack" | chpasswd && adduser localadmin sudo
USER localadmin
RUN echo 'export LC_ALL=zh_TW.utf8' >> /home/localadmin/.bashrc
#RUN cd
#CMD /bin/bash

# IPFS
RUN cd && \
wget https://dist.ipfs.io/go-ipfs/v0.4.13/go-ipfs_v0.4.13_linux-amd64.tar.gz && \
tar xvfz go-ipfs_v0.4.13_linux-amd64.tar.gz


# clone github project
RUN cd && \
git clone https://github.com/yenkuanlee/Ethereum-Contract-Web3 && \
cd Ethereum-Contract-Web3/VoteEX && \
cp vote.db /tmp && \
javac -cp ../json.jar:../servlet-api.jar *.java && \
cd ../AnswerGame && \
javac -cp ../json.jar:../servlet-api.jar *.java && \
cd ../User && \
javac -cp ../json.jar:../servlet-api.jar *.java && \
cd ../Application && \
javac -cp ../json.jar:../servlet-api.jar *.java

# tomcat setting
USER root
RUN cd /home/localadmin/Ethereum-Contract-Web3/VoteEX && \
mkdir /opt/tomcat7/webapps/ROOT/WEB-INF/classes && \
mv *.class /opt/tomcat7/webapps/ROOT/WEB-INF/classes && \
mv ../AnswerGame/*.class /opt/tomcat7/webapps/ROOT/WEB-INF/classes && \
mv ../User/*.class /opt/tomcat7/webapps/ROOT/WEB-INF/classes && \
mv ../Application/*.class /opt/tomcat7/webapps/ROOT/WEB-INF/classes && \
cp ../web.xml /opt/tomcat7/webapps/ROOT/WEB-INF && \
cp ../*.jar /opt/tomcat7/lib && \
cp -r blockVote /opt/tomcat7/webapps && \
cp -r ../AnswerGame/answerGame /opt/tomcat7/webapps && \
mv /home/localadmin/go-ipfs/ipfs /usr/local/bin/ipfs

# launch IPFS
USER localadmin
RUN ipfs init && \
sed -i 's/8080/8081/g' /home/localadmin/.ipfs/config
