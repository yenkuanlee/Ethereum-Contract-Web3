import json
from web3 import Web3, HTTPProvider, TestRPCProvider
from web3.contract import ConciseContract
import os
import sqlite3
conn = sqlite3.connect('/tmp/vote.db')
c = conn.cursor()
Cpath = os.path.dirname(os.path.realpath(__file__))

host = '150.117.122.84'
account = '0xe55879e12514f2255e6f4fd36bd459f0807de3b2'
passwd = '123'

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':8545'))
w3.personal.unlockAccount(account,passwd)
f = open(Cpath+'/users.json','r')
line = f.readline()
Jline = json.loads(line)
f.close()

abi = Jline['abi']
contract_address = Jline['contract_address']


# Contract instance in concise mode
contract_instance = w3.eth.contract(abi, contract_address, ContractFactoryClass=ConciseContract)

# name, ehash, host, passwd, tag, role
#contract_instance.setNode('name','ehash','host','passwd','tag','role', transact={'from': account})
load = c.execute("select * from user where Upasswd != 'null';")
for x in load:
    contract_instance.setNode(x[2],x[0],x[1],x[3],x[4],x[5], transact={'from': account})
