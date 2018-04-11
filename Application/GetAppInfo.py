import json
import subprocess
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys
import os
import ObjectNode

application = sys.argv[1]

# Set Peer
MCU = ObjectNode.ObjectNode("MCU")
accountPeer = MCU.ObjectPeer("account")
propPeer = MCU.ObjectPeer("prop")
deadlinePeer = MCU.ObjectPeer("deadline")

# Set Index
IndexDict = dict()
IndexDict[accountPeer] = "account"
IndexDict[propPeer] = "prop"
IndexDict[deadlinePeer] = "deadline"

Cpath = os.path.dirname(os.path.realpath(__file__))

host = '150.117.122.84'
account = '0xe55879e12514f2255e6f4fd36bd459f0807de3b2'
passwd = '123'

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':8545'))
w3.personal.unlockAccount(account,passwd)
f = open(Cpath+'/app.json','r')
line = f.readline()
Jline = json.loads(line)
f.close()

abi = Jline['abi']
contract_address = Jline['contract_address']


# Contract instance in concise mode
contract_instance = w3.eth.contract(abi, contract_address, ContractFactoryClass=ConciseContract)
###contract_instance.setNode("Vote","QmWvMxzFoKjUh4nF9Knf5XSYguVgzArzVZcsNXUJComLvD", transact={'from': account})
###print(contract_instance.GetOhash("Vote"))
AppHash = contract_instance.GetOhash(application)
cmd = "timeout 10 ipfs object get "+AppHash
output = subprocess.check_output(cmd, shell=True)
Joutput = json.loads(output.decode("utf-8"))

Jlist = list()
for x in Joutput['Links']:
    Jdict = dict()
    Jdict['contract_address'] = x['Name']
    cmd = "timeout 10 ipfs object get "+x['Hash']
    print(x['Hash'])
    output = subprocess.check_output(cmd, shell=True)
    J = json.loads(output.decode("utf-8"))
    Jdict['topic'] = J['Data']
    for y in J['Links']:
        Jdict[IndexDict[y['Hash']]] = y['Name']
    Jlist.append(Jdict)
    #print(Jdict)

print(json.dumps(Jlist))
