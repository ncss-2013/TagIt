import os
import sqlite3

if True: #not os.path.exists("database.db"):
    conn = sqlite3.connect("database.db")
    curs = conn.cursor()
    curs.executescript(open("database.sql").read())
    conn.commit()
    conn.close()
else:
    print("Database exists")
