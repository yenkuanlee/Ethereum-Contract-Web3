import sqlite3
conn = sqlite3.connect('/tmp/vote.db')
c = conn.cursor()
c.execute("create table if not exists User(Uhash text, Uname text);")

f = open("AllUser.txt","r")
while True:
    line = f.readline()
    if not line:
        break
    line = line.replace("\n","")
    tmp = line.split("\t")
    c.execute("insert into User values('"+tmp[1]+"','voter"+tmp[0]+"');")
    conn.commit()
