import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys
import os
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

Uname = sys.argv[1]
op = sys.argv[2]
np = sys.argv[3]
contract_instance.ModifyPasswd(Uname,op,np, transact={'from': account})
#print('Contract value: {}'.format(contract_instance.ModifyPasswd(Uname,op,np, transact={'from': account})))
