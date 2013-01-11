import sqlite3
conn = sqlite3.connect("test.db")
cursor = conn.cursor()
cursor.executescript("""
DROP TABLE IF EXISTS tab_name;
CREATE TABLE tab_name (id INT PRIMARY KEY, name TEXT);

""")
cursor.executescript("""
INSERT INTO tab_name VALUES (1, "Caspar");
INSERT INTO tab_name VALUES (2, "Jess");
INSERT INTO tab_name VALUES (3, "Alex");
""")
conn.commit()
cursor.execute("SELECT * FROM tab_name")
for row in cursor:
    print(row)
cursor.close()
conn.close()
