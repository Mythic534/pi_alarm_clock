import sqlite3

def connect():
    return sqlite3.connect("alarms.db")

def init_db():
    con = connect()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS alarms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        enabled INTEGER DEFAULT 1,
        datetime TEXT,
        name TEXT,
        recurring INTEGER,
        recurring_days TEXT
    );
    """)

    con.commit()
    con.close()

"""cur.execute("INSERT INTO alarms (datetime, name, recurring, recurring_days) VALUES (?, ?, ?, ?)",
            ("2026-05-26 07:30", "Test", 0, None))"""

def get_alarms():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT id, enabled, datetime, name, recurring, recurring_days FROM alarms")
    rows = cur.fetchall()
    con.close()
    return rows