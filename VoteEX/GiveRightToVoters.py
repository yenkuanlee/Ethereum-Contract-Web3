import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys
import os

Cpath = os.path.dirname(os.path.realpath(__file__))

#host = '150.117.122.81'
#account = '0x12a74e70f5c207d17b869daae374accc1a66eebc'
#passwd = 'OR51M59'
#contract_address = '0x412Ee1F24EEC96B0c697826E1d0f291b0C04aFF3'
host = sys.argv[1]
account = sys.argv[2]
passwd = sys.argv[3]
contract_address = sys.argv[4]
#voter = '0xf6f5d7024cfc89232afa6453ec70d9df92f7825c'

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':3000'))
w3.personal.unlockAccount(account,passwd)

f = open(Cpath+'/abi','r')
abi = f.readline()
f.close()
abi = json.loads(abi)


# Contract instance in concise mode

contract_instance = w3.eth.contract(abi, contract_address, ContractFactoryClass=ConciseContract)

try:
    OneVoter = sys.argv[5]
    contract_instance.giveRightToVote(OneVoter,transact={'from': account})
except:
    print("Load All Users")
    f = open(Cpath+'/AllUser.txt','r')
    while True:
        line = f.readline()
        if not line:
            break
        voter = line.replace("\n","").split("\t")[1]
        contract_instance.giveRightToVote(voter,transact={'from': account})

