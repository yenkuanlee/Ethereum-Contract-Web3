import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys
import sqlite3
import os
Cpath = os.path.dirname(os.path.realpath(__file__))

host = sys.argv[1]
contract_address = sys.argv[2]

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':8545'))
f = open(Cpath+'/abi','r')
abi = f.readline()
f.close()
abi = json.loads(abi)

contract_instance = w3.eth.contract(abi, contract_address, ContractFactoryClass=ConciseContract)

conn = sqlite3.connect('/tmp/vote.db')
c = conn.cursor()
c.execute("create table if not exists Vote(contract_address text, account text, topic text, _numProposals int, prop text);")
tmp = c.execute("select * from Vote where contract_address = '"+contract_address+"';")
for x in tmp:
    Jstatus = json.loads(x[len(x)-1])
    for y in Jstatus:
        #print(Jstatus[y]["num"])
        #print(contract_instance.GetVoteCount(int(Jstatus[y]["num"])))
        Jstatus[y]["cnt"] = int(contract_instance.GetVoteCount(int(Jstatus[y]["num"])))
    print(Jstatus)
c.execute("update Vote set prop = '"+json.dumps(Jstatus)+"' where contract_address = '"+contract_address+"';")
conn.commit()