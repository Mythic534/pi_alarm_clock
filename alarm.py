#!/usr/bin/env python3

import typer
import database as db

db.init_db()
app = typer.Typer()

def manage():
    alarms = db.get_alarms()

    print("\nID | DATETIME | NAME | RECURRING | RECURRING_DAYS | ENABLED")
    print("-" * 60)

    for a in alarms:
        print(f"{a[0]} | {a[1]} | {a[2]} | {a[3]} | {a[4]} | {a[5]}")

@app.command()
def add(time: str):
    """Add an alarm to database"""
    print(f"Adding alarm at {time}")

@app.command()
def view():
    print(f"Viewing alarms")
    manage()

@app.command()
def disable():
    print(f"Disabling alarms")
    manage()

@app.command()
def remove():
    print(f"Removing alarms")
    manage()

app()