from web3 import Web3, HTTPProvider
web3 = Web3(HTTPProvider('http://150.117.122.84:8545'))
god = "0xe55879e12514f2255e6f4fd36bd459f0807de3b2"
f = open("AllUser.txt","r")
while True:
    line = f.readline()
    if not line:break
    user = line.split("\t")[1].split("\n")[0]
    web3.personal.unlockAccount(god, '123')
    web3.eth.sendTransaction({"to": user, "from": god,"value":web3.toWei("1000", "ether")})
f.close()
