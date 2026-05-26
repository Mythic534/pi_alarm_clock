import database as db

db.init_db()

con = db.connect()
cur = con.cursor()

cur.execute("INSERT INTO alarms (datetime, name, recurring, recurring_days) VALUES (?, ?, ?, ?)",
            ("2026-05-27 09:15", "Test", 0, None))

con.commit()
con.close() 