import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract

host = '150.117.122.84'
account = '0x3b48ba756fb58492ea9cfca48df123fc09bee72b'
passwd = '123'

f = open('test.sol','r')
X = ""
while True:
    line = f.readline()
    if not line:
        break
    X += line
contract_source_code = X

compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:test']

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':3000'))
w3.personal.unlockAccount(account, passwd)
# Instantiate and deploy contract
contractt = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Get transaction hash from deployed contract
sign_hash = "0x76dc9ebcaf935bfe84182b6c4f15153cfdb3f4f41f4602113b4912084cde4bc751cefda24a093b4656370fb047d69f19efd5bc515460e6730d28a8b1c9f03e581c"
tx_hash = contractt.deploy(transaction={'from': account, 'gas': 4000000})
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
###print(contract_instance)

Joutput = dict()
fw = open('test.json','w')
Joutput['abi'] = contract_interface['abi']
Joutput['contract_address'] = contract_address
fw.write(json.dumps(Joutput))
fw.close()

print("account : "+account)
print("contract address : "+contract_address)
print("contract abi : "+json.dumps(contract_interface['abi']))

# Getters + Setters for web3.eth.contract object
###print('Contract value: {}'.format(contract_instance.greet()))
'''
contract_instance.setNode('123','kevin', transact={'from': account})
time.sleep(10)
print('Setting value to: Nihao')
print('Contract value: {}'.format(contract_instance.greet("123")))
'''
