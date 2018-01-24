import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys

#host = '150.117.122.81'
#account = '0x99c4e099a0a1e35769865295c69dca628ea172b0'
#passwd = 'OR51M00'
#contract_address = '0x3a4828415A86ce9AC5C5F61E904F192A401aD1F6'
host = sys.argv[1]
account = sys.argv[2]
passwd = sys.argv[3]
contract_address = sys.argv[4]
answer = sys.argv[5]

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':8545'))
w3.personal.unlockAccount(account,passwd)
abi = '[{"name": "endTime", "payable": false, "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "type": "function", "constant": true, "stateMutability": "view"}, {"name": "checkList", "payable": false, "inputs": [{"name": "_password", "type": "bytes32"}], "outputs": [{"name": "_List", "type": "address[10]"}], "type": "function", "constant": true, "stateMutability": "view"}, {"name": "standard", "payable": false, "inputs": [], "outputs": [{"name": "", "type": "string"}], "type": "function", "constant": true, "stateMutability": "view"}, {"name": "sendAnswer", "payable": false, "inputs": [{"name": "_answer", "type": "string"}], "outputs": [], "type": "function", "constant": false, "stateMutability": "nonpayable"}, {"name": "checkAnswer", "payable": false, "inputs": [{"name": "_password", "type": "bytes32"}], "outputs": [{"name": "_answer", "type": "string"}], "type": "function", "constant": true, "stateMutability": "view"}, {"name": "creationTime", "payable": false, "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "type": "function", "constant": true, "stateMutability": "view"}, {"type": "constructor", "payable": false, "inputs": [{"name": "_answer", "type": "string"}, {"name": "_password", "type": "bytes32"}, {"name": "_duration", "type": "uint256"}], "stateMutability": "nonpayable"}]'
abi = json.loads(abi)


# Contract instance in concise mode

contract_instance = w3.eth.contract(abi, contract_address, ContractFactoryClass=ConciseContract)

#w3.personal.unlockAccount(account, passwd)
contract_instance.sendAnswer(answer,transact={'from': account})

#print(contract_instance.checkAnswer(passwd))
#print(contract_instance.checkList(passwd))

