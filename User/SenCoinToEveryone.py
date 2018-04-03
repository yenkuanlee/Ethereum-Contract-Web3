from web3 import Web3, HTTPProvider
web3 = Web3(HTTPProvider('http://150.117.122.81:8545'))
god = "0x3b48ba756fb58492ea9cfca48df123fc09bee72b"
f = open("AllUser.txt","r")
while True:
    line = f.readline()
    user = line.split("\t")[1].split("\n")[0]
    web3.personal.unlockAccount(god, '123')
    web3.eth.sendTransaction({"to": user, "from": god,"value":web3.toWei("10000", "ether")})
f.close()
