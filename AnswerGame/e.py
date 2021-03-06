# -*- coding: utf-8 -*- 
import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys

host = sys.argv[1]
passwd = sys.argv[2]
contract_address = sys.argv[3]
behavior = sys.argv[4]

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':3000'))
abi = '[{"name": "endTime", "payable": false, "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "type": "function", "constant": true, "stateMutability": "view"}, {"name": "checkList", "payable": false, "inputs": [{"name": "_password", "type": "bytes32"}], "outputs": [{"name": "_List", "type": "address[10]"}], "type": "function", "constant": true, "stateMutability": "view"}, {"name": "standard", "payable": false, "inputs": [], "outputs": [{"name": "", "type": "string"}], "type": "function", "constant": true, "stateMutability": "view"}, {"name": "sendAnswer", "payable": false, "inputs": [{"name": "_answer", "type": "string"}], "outputs": [], "type": "function", "constant": false, "stateMutability": "nonpayable"}, {"name": "checkAnswer", "payable": false, "inputs": [{"name": "_password", "type": "bytes32"}], "outputs": [{"name": "_answer", "type": "string"}], "type": "function", "constant": true, "stateMutability": "view"}, {"name": "creationTime", "payable": false, "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "type": "function", "constant": true, "stateMutability": "view"}, {"type": "constructor", "payable": false, "inputs": [{"name": "_answer", "type": "string"}, {"name": "_password", "type": "bytes32"}, {"name": "_duration", "type": "uint256"}], "stateMutability": "nonpayable"}]'
abi = json.loads(abi)


# Contract instance in concise mode

contract_instance = w3.eth.contract(abi, contract_address, ContractFactoryClass=ConciseContract)

if behavior=='checkAnswer':
    outputA = contract_instance.checkAnswer(passwd)
    print("尚未公佈")
elif behavior=='checkList':
    print(json.dumps(contract_instance.checkList(passwd)))

