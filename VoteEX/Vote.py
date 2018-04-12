import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys
import os
Cpath = os.path.dirname(os.path.realpath(__file__))

#host = '150.117.122.81'
#account = '0x75cbef652f58d31031b6000bb80a80c77bba7079'
#passwd = 'OR51L12'
#contract_address = '0x412Ee1F24EEC96B0c697826E1d0f291b0C04aFF3'
host = sys.argv[1]
account = sys.argv[2]
passwd = sys.argv[3]
contract_address = sys.argv[4]
to_Voter = sys.argv[5]
cnt = sys.argv[6]

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':3000'))
w3.personal.unlockAccount(account,passwd)
f = open(Cpath+'/abi','r')
abi = f.readline()
f.close()
abi = json.loads(abi)


# Contract instance in concise mode

contract_instance = w3.eth.contract(abi, contract_address, ContractFactoryClass=ConciseContract)

#w3.personal.unlockAccount(account, passwd)
contract_instance.vote(int(to_Voter),int(cnt),transact={'from': account})

#print(contract_instance.checkAnswer(passwd))
#print(contract_instance.checkList(passwd))

