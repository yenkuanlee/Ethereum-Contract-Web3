import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys
import os
Cpath = os.path.dirname(os.path.realpath(__file__))

host = '150.117.122.81'
account = '0x7893edc24aafc52cacb6b6ec65091d22293eb66c'
passwd = '123'

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':8545'))
w3.personal.unlockAccount(account,passwd)
f = open(Cpath+'/app.json','r')
line = f.readline()
Jline = json.loads(line)
f.close()

abi = Jline['abi']
contract_address = Jline['contract_address']


# Contract instance in concise mode
contract_instance = w3.eth.contract(abi, contract_address, ContractFactoryClass=ConciseContract)
#contract_instance.setNode("Vote","QmWvMxzFoKjUh4nF9Knf5XSYguVgzArzVZcsNXUJComLvD", transact={'from': account})
print(contract_instance.GetOhash("Vote"))
