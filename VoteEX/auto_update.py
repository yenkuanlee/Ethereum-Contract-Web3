import sqlite3
import os
import time

while True:
    conn = sqlite3.connect('/tmp/vote.db')
    c = conn.cursor()
    tmp = c.execute("select contract_address from Vote;")
    Clist = list()
    for x in tmp:
        Clist.append(x[0])
    conn.close()

    for x in Clist:
        os.system("python3 Update.py 150.117.122.83 "+x)
    time.sleep(1)
