import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys
import sqlite3

host = '150.117.122.81'
account = '0x12a74e70f5c207d17b869daae374accc1a66eebc'
passwd = 'OR51M59'
#host = sys.argv[1]
#account = sys.argv[2]
#passwd = sys.argv[3]
_numProposals = 3


# Solidity source code
f = open('votes.sol','r')
contract_source_code = ""
while True:
    line = f.readline()
    if not line:
        break
    contract_source_code += line


compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:Ballot']

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':3000'))
w3.personal.unlockAccount(account, passwd)
# Instantiate and deploy contract
contractt = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Get transaction hash from deployed contract
tx_hash = contractt.deploy(args=[_numProposals],transaction={'from': account, 'gas': 4000000})
###print(tx_hash)

# Get tx receipt to get contract address
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

cnt = 1
while True:
	if tx_receipt == None:
		print("wait...("+str(cnt)+")")
		cnt += 1
		time.sleep(1)
		tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
	else:
		break

###print(tx_receipt)
contract_address = tx_receipt['contractAddress']

# Contract instance in concise mode
contract_instance = w3.eth.contract(contract_interface['abi'], contract_address, ContractFactoryClass=ConciseContract)

print("account : "+account)
print("contract address : "+contract_address)
print("contract abi : "+json.dumps(contract_interface['abi']))


'''
conn = sqlite3.connect('/tmp/answer_game.db')
c = conn.cursor()
c.execute("create table if not exists question_list(contract_address text, abi text, account text, question text, answer text, deadline text);")

c.execute("insert into question_list values('"+contract_address+"','"+json.dumps(contract_interface['abi'])+"','"+account+"','"+question+"','"+answer+"','"+str(duration)+"');")
conn.commit()
'''
