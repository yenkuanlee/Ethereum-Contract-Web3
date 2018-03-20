import sqlite3
conn = sqlite3.connect('/tmp/vote.db')
c = conn.cursor()

fw = open('AllUser.txt','w')
load = c.execute("select host,Uhash from user where Upasswd != 'null';")
for x in load:
    fw.write(x[0]+"\t"+x[1]+"\n")
fw.close()
