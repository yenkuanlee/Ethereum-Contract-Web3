import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys

host = '150.117.122.81'
account = '0x58990d5f96427bd5d03d54518d8d88ca14e1d420'
passwd = 'OR51Z12'
contract_address = '0x4F716227259E5FA2f97aF702cAfA8d5978Abf80e'
#host = sys.argv[1]
#account = sys.argv[2]
#passwd = sys.argv[3]
#contract_address = sys.argv[4]

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':8545'))
w3.personal.unlockAccount(account,passwd)
f = open('abi','r')
abi = f.readline()
f.close()
abi = json.loads(abi)


# Contract instance in concise mode

contract_instance = w3.eth.contract(abi, contract_address, ContractFactoryClass=ConciseContract)

#w3.personal.unlockAccount(account, passwd)
contract_instance.vote(1,transact={'from': account})

#print(contract_instance.checkAnswer(passwd))
#print(contract_instance.checkList(passwd))

