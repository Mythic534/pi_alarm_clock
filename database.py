import sqlite3

con = sqlite3.connect("alarms.db")
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS alarms (
id INTEGER PRIMARY KEY AUTOINCREMENT,
datetime TEXT,
name TEXT,
recurring INTEGER,
recurring_weekdays TEXT,
enabled INTEGER DEFAULT 1
);""")

con.commit()
con.close()