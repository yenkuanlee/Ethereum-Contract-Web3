from web3 import Web3, HTTPProvider
f = open('host','r')
fw = open("AllUser.txt","w")
while True:
    line = f.readline()
    host = line.replace("\n","")
    web3 = Web3(HTTPProvider('http://'+host+':3000'))
    god = web3.eth.coinbase
    web3.personal.unlockAccount(god, '123')
    for i in range(30):
        Ehash = web3.personal.newAccount("123")
        web3.eth.sendTransaction({"to": Ehash, "from": god,"value":web3.toWei("1000", "ether")})
        fw.write(host+"\t"+Ehash+"\n")
f.close()
fw.close()
