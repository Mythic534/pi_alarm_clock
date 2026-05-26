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

cur.execute("INSERT INTO alarms (datetime, name, recurring, recurring_weekdays) VALUES (?, ?, ?, ?)",
            ("2026-05-26 07:30", "Test", 0, None))

con.commit()
con.close()