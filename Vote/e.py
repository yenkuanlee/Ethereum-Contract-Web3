import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys

host = '150.117.122.81'
#account = '0x12a74e70f5c207d17b869daae374accc1a66eebc'
passwd = 'OR51M59'
contract_address = '0x4F716227259E5FA2f97aF702cAfA8d5978Abf80e'
#host = sys.argv[1]
#passwd = sys.argv[2]
#contract_address = sys.argv[3]

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':8545'))
f = open('abi','r')
abi = f.readline()
f.close()
abi = json.loads(abi)


# Contract instance in concise mode

contract_instance = w3.eth.contract(abi, contract_address, ContractFactoryClass=ConciseContract)

print(contract_instance.winningProposal())

