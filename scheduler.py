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
        if candidate <= today:
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


def run_scheduler():

    last_fired_dt = None
    while True:

        next_alarm = get_next_alarm()
        if next_alarm:
            seconds_until = (next_alarm['datetime'] - datetime.datetime.now()).total_seconds()

            if -3 <= seconds_until <= 1:
                if last_fired_dt != next_alarm['datetime']:
                    last_fired_dt = next_alarm['datetime']
                    player.sound_alarm()
                    time.sleep(20)

            elif seconds_until < -3:
                time.sleep(5)

            else:
                time.sleep(min(seconds_until - 1, 30))

        else:
            last_fired_dt = None
            time.sleep(30)


if __name__ == "__main__":
    run_scheduler()