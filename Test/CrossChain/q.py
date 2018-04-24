import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract

host = '150.117.122.84'
account = '0x3b48ba756fb58492ea9cfca48df123fc09bee72b'
passwd = '123'


# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':3000'))
w3.personal.unlockAccount(account, passwd)
aaaa = w3.eth.sign(account, text = '123')

print(aaaa)

