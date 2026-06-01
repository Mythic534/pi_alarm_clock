import database as db

db.init_db()

con = db.connect()
cur = con.cursor()


# One off

"""cur.execute("INSERT INTO alarms (datetime, name, recurring, recurring_days) VALUES (?, ?, ?, ?)",
            ("2026-05-31 23:50", "Test1", 0, None))
"""
 
# Recurring
"""
cur.execute("INSERT INTO alarms (datetime, name, recurring, recurring_days) VALUES (?, ?, ?, ?)",
            ("2026-05-27 10:00", "Test2", 1, "Mon,Tue,Wed,Thu,Fri,Sat,Sun"))

"""
cur.execute("INSERT INTO alarms (datetime, name, recurring, recurring_days) VALUES (?, ?, ?, ?)",
            ("2026-06-05 01:00", "Test4", 1, "Mon"))


con.commit()
con.close() 