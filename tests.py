import database as db

db.init_db()

con = db.connect()
cur = con.cursor()


# One off

cur.execute("INSERT INTO alarms (datetime, name, recurring, recurring_days) VALUES (?, ?, ?, ?)",
            ("2026-06-01 04:55", "Test1", 0, None))

 
# Recurring
"""
cur.execute("INSERT INTO alarms (datetime, name, recurring, recurring_days) VALUES (?, ?, ?, ?)",
            ("2026-05-27 10:00", "Test2", 1, "Mon,Tue,Wed,Thu,Fri,Sat,Sun"))

"""
cur.execute("INSERT INTO alarms (datetime, name, recurring, recurring_days) VALUES (?, ?, ?, ?)",
            ("2026-05-01 04:15", "Test4", 1, "Mon,Wed"))


con.commit()
con.close() 
