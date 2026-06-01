#!/usr/bin/env python3

import typer
import database as db
from datetime import datetime

db.init_db()
app = typer.Typer()

@app.command()
def view():
    alarms = db.get_alarms()

    print("\nID    | ENABLED  | DATETIME         | NAME         | RECURRING  | RECURRING_DAYS")
    print("-" * 80)

    for a in alarms:
        alarm_id = a[0]
        enabled = "On " if a[1] else "Off"
        dt = datetime.fromisoformat(a[2]).strftime('%d/%m/%Y %H:%M')
        name = f"{a[3][:12]:<12}"
        recurring = "Yes" if a[4] else "No "
        recurring_days = a[5] if a[5] else "-"

        print(f"{alarm_id:04d}  | {enabled}      | {dt} | {name} | {recurring}        | {recurring_days}")

    print("\n")


@app.command()
def add():
    view()

    name = typer.prompt("Alarm name")
    recurring = typer.confirm("Recurring alarm?", default=False)

    recurring_days = None
    if recurring:
        recurring_days = typer.prompt("Recurring days (comma separated, e.g. Mon,Tue,Wed)")
        date = datetime.today()
    else:
        date_str = typer.prompt("Alarm date (DD-MM-YYYY) or leave blank for today", default="")
        date = datetime.today() if date_str.strip() == "" else datetime.strptime(date_str, "%d-%m-%Y")

    time_str = typer.prompt("Alarm time (HH:MM)")

    try:
        alarm_dt = datetime.strptime(f"{date.strftime('%Y-%m-%d')} {time_str}", "%Y-%m-%d %H:%M")
    except ValueError as e:
        typer.echo(f"Invalid date or time: {e}")
        raise typer.Exit(1)

    db.add_alarm(
        dt=alarm_dt.isoformat(timespec="seconds"),
        name=name,
        recurring=int(recurring),
        recurring_days=recurring_days
    )

    typer.echo(f"\nAdded alarm '{name}' at {alarm_dt.strftime('%d/%m/%Y %H:%M')}")
    view()


@app.command()
def disable():
    view()
    alarm_id = typer.prompt("Enter ID of alarm to disable")
    db.disable_alarm(alarm_id)
    typer.echo(f"Disabled alarm {alarm_id}")
    view()


@app.command()
def remove():
    view()
    alarm_id = typer.prompt("Enter ID of alarm to remove")
    db.remove_alarm(alarm_id)
    typer.echo(f"Removed alarm {alarm_id}")
    view()


@app.command()
def manage():
    view()


app()