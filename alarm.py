#!/usr/bin/env python3

import typer
import database as db

db.init_db()
app = typer.Typer()

@app.command()
def manage():
    alarms = db.get_alarms()

    print("\nID | ENABLED  | DATETIME         | NAME | RECURRING  | RECURRING_DAYS")
    print("-" * 70)

    for a in alarms:
        alarm_id = a[0]
        enabled = "On " if a[1] else "Off"
        dt = a[2]
        name = a[3]
        recurring = "Yes" if a[4] else "No "
        recurring_days = a[5] if a[5] else "-"

        print(f"{alarm_id}  | {enabled}      | {dt} | {name} | {recurring}        | {recurring_days}")

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