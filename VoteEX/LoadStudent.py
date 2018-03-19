import sqlite3
conn = sqlite3.connect('/tmp/vote.db')
c = conn.cursor()

Slist = list()
f = open('student','r')
while True:
    line = f.readline()
    if not line:
        break
    line = line.replace("\n","")
    tmp = line.split("\t")
    Slist.append((tmp[0],tmp[1]))

load = c.execute("select Uname from user where tag='null' limit "+str(len(Slist))+";")
Ulist = list()
for x in load:
    Ulist.append(x[0])

for i in range(len(Slist)):
    try:
        c.execute("update user set Uname = '"+Slist[i][1]+"',Upasswd='"+Slist[i][1]+"',tag='C"+Slist[i][0]+"',role='student' where Uname = '"+Ulist[i]+"';")
        conn.commit()
    except:
        print Slist[i]
