import subprocess
import ObjectNode
import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys
import sqlite3
import os
Cpath = os.path.dirname(os.path.realpath(__file__))

def AddHash(Ahash, Bhash,ObjectName):
    cmd = "timeout 10 ipfs object patch add-link "+Ahash+" "+ObjectName+" "+Bhash
    output = "OUTPUT ERROR"
    try:
        output = subprocess.check_output(cmd, shell=True)
        output = output.decode("utf-8")
        if "Error" in output:
            return output
    except:
        return output
    NewOhash = output.split("\n")[0]
    cmd = "timeout 10 ipfs pin add "+NewOhash
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode("utf-8")
    if "Error" in output:
        return output
    return NewOhash

#host = '150.117.122.81'
#account = '0x12a74e70f5c207d17b869daae374accc1a66eebc'
#passwd = 'OR51M59'
host = sys.argv[1]
account = sys.argv[2]
passwd = sys.argv[3]
topic = sys.argv[4]
_numProposals = int(sys.argv[5])
prop = sys.argv[6]
deadline = sys.argv[7]
Pdict = dict()
Plist = prop.split(",,,")
num = 0
Nprop = ""
for x in Plist:
    picture = "NULL"
    key = x.split("@@")[0]
    Nprop += key+",,,"
    try:
        picture = x.split("@@")[1]
    except:
        pass
    Pdict[key] = dict()
    Pdict[key]["num"] = num
    Pdict[key]["cnt"] = 0
    Pdict[key]["picture"] = picture
    num += 1
prop = Nprop[:-3]

# Solidity source code
f = open(Cpath+'/votes.sol','r')
contract_source_code = ""
while True:
    line = f.readline()
    if not line:
        break
    contract_source_code += line


compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:Ballot']
f = open(Cpath+'/abi','w')
f.write(json.dumps((contract_interface['abi'])))
f.close()

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



conn = sqlite3.connect('/tmp/vote.db')
c = conn.cursor()
c.execute("create table if not exists Vote(contract_address text, account text, topic text, _numProposals int, prop text, deadline text);")

c.execute("insert into Vote values('"+contract_address+"','"+account+"','"+topic+"',"+str(_numProposals)+",'"+json.dumps(Pdict)+"', '"+deadline+"');")
conn.commit()


f = open('/home/localadmin/Ethereum-Contract-Web3/Application/app.json','r')
line = f.readline()
Jline = json.loads(line)
f.close()

Aabi = Jline['abi']
Acontract_address = Jline['contract_address']
Acontract_instance = w3.eth.contract(Aabi, Acontract_address, ContractFactoryClass=ConciseContract)

import ObjectNode
MCU = ObjectNode.ObjectNode("MCU")
accountPeer = MCU.ObjectPeer("account")
propPeer = MCU.ObjectPeer("prop")
deadlinePeer = MCU.ObjectPeer("deadline")

#Vgod = ObjectNode.ObjectNode("Vote") ### will retrive from smart contract
VoteHash = Acontract_instance.GetOhash("Vote")

a = ObjectNode.ObjectNode(topic)
a.AddHash(accountPeer,account)
a.AddHash(propPeer,prop)
a.AddHash(deadlinePeer,deadline)
NewHash = AddHash(VoteHash,a.ObjectHash,contract_address)
Acontract_instance.setNode("Vote",NewHash, transact={'from': account})
os.system("timeout 10 ipfs pin add "+NewHash)
