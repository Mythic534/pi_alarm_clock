#!/usr/bin/env python3

import typer
import database as db

db.init_db()
app = typer.Typer()

def manage():
    alarms = db.get_alarms()

    print("\nID | DATETIME         | NAME | RECURRING | RECURRING_DAYS | ENABLED")
    print("-" * 70)

    for a in alarms:
        alarm_id = a[0]
        dt = a[1]
        name = a[2]
        recurring = "Yes" if a[3] else "No"
        recurring_days = a[4] if a[4] else "-"
        enabled = "On" if a[5] else "Off"

        print(f"{alarm_id}  | {dt} | {name} | {recurring}        | {recurring_days} | {enabled}")

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