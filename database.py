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


def get_alarms():
    con = connect()
    cur = con.cursor()

    cur.execute("SELECT id, enabled, datetime, name, recurring, recurring_days FROM alarms")
    rows = cur.fetchall()
    con.close()
    return rows


def get_enabled_alarms():
    con = connect()
    cur = con.cursor()

    cur.execute("SELECT id, enabled, datetime, name, recurring, recurring_days FROM alarms WHERE enabled = 1")
    rows = cur.fetchall()
    con.close()
    return rows


def remove_alarm(alarm_id):
    con = connect()
    cur = con.cursor()

    cur.execute("DELETE FROM alarms WHERE id = ?", (alarm_id,))
    con.commit()
    con.close()