import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract

host = '150.117.122.81'
account = '0x12a74e70f5c207d17b869daae374accc1a66eebc'
passwd = 'OR51M59'

# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.0;

contract Greeter {
    string public greeting;
    function Greeter(string _tmp) {
        greeting = _tmp;
    }

    function setGreeting(string _greeting) public {
        greeting = _greeting;
    }

    function greet() constant returns (string) {
        return greeting;
    }
}
'''


compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:Greeter']

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':8545'))
w3.personal.unlockAccount(account, passwd)
# Instantiate and deploy contract
contractt = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Get transaction hash from deployed contract
tx_hash = contractt.deploy(args=['ppp'],transaction={'from': account, 'gas': 4000000})
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

# Getters + Setters for web3.eth.contract object
print('Contract value: {}'.format(contract_instance.greet()))
contract_instance.setGreeting('Nihao', transact={'from': account})
time.sleep(10)
print('Setting value to: Nihao')
print('Contract value: {}'.format(contract_instance.greet()))

