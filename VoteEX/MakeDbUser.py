import sqlite3
conn = sqlite3.connect('/tmp/vote.db')
c = conn.cursor()
c.execute("create table if not exists User(Uhash text, host text, Uname text, Upasswd text, tag text, role text, PRIMARY KEY(Uname));")

f = open("AllUser.txt","r")
cnt = 0
while True:
    line = f.readline()
    if not line:
        break
    cnt += 1
    line = line.replace("\n","")
    tmp = line.split("\t")
    c.execute("insert into User values('"+tmp[1]+"','"+tmp[0]+"','voter"+str(cnt)+"','null','null','null');")
    conn.commit()
