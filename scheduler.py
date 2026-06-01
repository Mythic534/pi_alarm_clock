import datetime
import time

from database import get_enabled_alarms
from player import player


def next_occurrence(alarm):
    """Calculate the next occurrence of an alarm based on its recurring_days."""

    dt = datetime.datetime.fromisoformat(alarm[2])
    if not alarm[4]:  # not recurring
        return dt

    today = datetime.datetime.now()
    grace = datetime.timedelta(seconds=25)
    candidates = []

    for day in alarm[5].split(","):
        day_num = time.strptime(day.strip(), "%a").tm_wday

        days_ahead = (day_num - today.weekday()) % 7

        candidate = today + datetime.timedelta(days=days_ahead)
        candidate = candidate.replace(
            hour=dt.hour,
            minute=dt.minute,
            second=0,
            microsecond=0
        )

        # If alarm time has already passed today, move to the next week
        if candidate <= today - grace:
            candidate += datetime.timedelta(days=7)

        candidates.append(candidate)

    return min(candidates)


def get_next_alarm():
    """Return the next scheduled alarm as a dict with keys: name, time, day, date, datetime."""

    alarms = get_enabled_alarms()

    dt_list = []
    for alarm in alarms:
        alarm_dt = next_occurrence(alarm)

        if alarm_dt and alarm_dt >= datetime.datetime.now():
            dt_list.append((alarm_dt, alarm))

    if not dt_list:
        return None

    dt_list.sort(key=lambda x: x[0])
    alarm_dt, alarm = dt_list[0]
        
    return {
        "name": alarm[3],
        "time": alarm_dt.strftime("%H:%M"),
        "day":  alarm_dt.strftime("%a").upper(),
        "date": alarm_dt.strftime("%d %b %Y").upper(),
        "datetime": alarm_dt
    }


def alarm_due(alarm):
    now = datetime.datetime.now()
    return 0 <= (now - alarm['datetime']).total_seconds() <= 20


def check_alarm():
    """Check if any alarm is due and trigger it."""

    next_alarm = get_next_alarm()
    if next_alarm and alarm_due(next_alarm):
        player.sound_alarm()
        time.sleep(20)


"""def run_scheduler():
    while True:
        check_alarm()
        time.sleep(10)
"""
import traceback

def run_scheduler():
    while True:
        try:
            check_alarm()
        except Exception:
            traceback.print_exc()
        time.sleep(10)


if __name__ == "__main__":
    run_scheduler()