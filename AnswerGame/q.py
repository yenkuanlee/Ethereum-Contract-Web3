import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys
import sqlite3

#host = '150.117.122.81'
#account = '0x12a74e70f5c207d17b869daae374accc1a66eebc'
#passwd = 'OR51M59'
host = sys.argv[1]
account = sys.argv[2]
passwd = sys.argv[3]
question = sys.argv[4]
answer = sys.argv[5]
duration = 20200101
try:
    duration = int(sys.argv[6])
except:
    pass

# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.13;
contract answerGame {
    string public standard = 'answerGame 1.0';
    string answer;
    bytes32 password;
    address[10] correctList;
    uint public creationTime = now;
    uint public endTime;
    mapping (address => bool)  personOfcorrect;
    function stringsEqual(string storage _a, string memory _b) internal constant returns (bool) {
        bytes storage a = bytes(_a);
        bytes memory b = bytes(_b);
        if (a.length != b.length)
            return false;
        for (uint i = 0; i < a.length; i ++)
            if (a[i] != b[i])
                return false;
        return true;
    }
    function answerGame(string _answer, bytes32 _password, uint _duration) {
        answer = _answer;
        password = _password;
        endTime = now + _duration;
    }
    function sendAnswer(string _answer){
        if(personOfcorrect[msg.sender] || now >endTime){ 
            revert();
        }else if(stringsEqual(answer, _answer)){
            for(uint i=0;i<correctList.length;i++){
                if(correctList[i]==msg.sender){ // repeat answer
                    break;
                }
                if(correctList[i]==0x00){
                    correctList[i] = msg.sender;
                    break;
                }
            }
        }
    }
    function checkAnswer(bytes32 _password) constant returns (string _answer) {
        if(_password == password){
            return answer;
        }
    }
    function checkList(bytes32 _password) constant returns (address[10] _List){
        return correctList;
    }
}
'''


compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:answerGame']

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':3000'))
w3.personal.unlockAccount(account, passwd)
# Instantiate and deploy contract
contractt = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Get transaction hash from deployed contract
tx_hash = contractt.deploy(args=[answer.encode('latin-1', 'ignore'),passwd,duration],transaction={'from': account, 'gas': 4000000})
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
print("answer : "+answer)
print("deadline : "+str(duration))

'''
# Getters + Setters for web3.eth.contract object
print('Contract value: {}'.format(contract_instance.greet()))
contract_instance.setGreeting('Nihao', transact={'from': account})
time.sleep(10)
print('Setting value to: Nihao')
print('Contract value: {}'.format(contract_instance.greet()))
'''

conn = sqlite3.connect('/tmp/answer_game.db')
c = conn.cursor()
c.execute("create table if not exists question_list(contract_address text, abi text, account text, question text, answer text, deadline text);")

c.execute("insert into question_list values('"+contract_address+"','"+json.dumps(contract_interface['abi'])+"','"+account+"','"+question+"','"+answer+"','"+str(duration)+"');")
conn.commit()
