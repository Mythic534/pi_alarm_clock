"""
alarm-clock frontend — app.py
Flask server for the Pi 5 / Pi Touch Display 2 kiosk clock.

Assumes scheduler.py exposes:
  get_next_alarm() -> APScheduler Job | dict | None
    If a Job object:   uses job.next_run_time (datetime) and job.name / job.id
    If a dict:         expects keys  "name", "time" (HH:MM), "day" (e.g. "FRI"), "date" (e.g. "29 MAY 2026")
  stop_alarm()      -> called when the screen is touched while an alarm is sounding
                       (implement as needed — missing function is handled gracefully)
"""

from flask import Flask, render_template, jsonify
from datetime import datetime
import logging
import threading

from scheduler import get_next_alarm, run_scheduler
from player import player

class _StatusFilter(logging.Filter):
    """Filter out log spam."""
    def filter(self, record):
        return '/api/status' not in record.getMessage()

logging.getLogger('werkzeug').addFilter(_StatusFilter())

app = Flask(__name__)


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("clock.html")


@app.route("/api/status")
def api_status():
    """Polled every 500 ms by the frontend to refresh time and alarm."""
    now   = datetime.now()
    alarm = None

    try:
        alarm = get_next_alarm()
    except Exception as exc:
        app.logger.warning("get_next_alarm() raised: %s", exc)

    return jsonify({
        "time":  now.strftime("%H:%M:%S"),
        "day":   now.strftime("%a").upper(),
        "date":  now.strftime("%d %b %Y").upper(),
        "alarm": alarm,
    })


@app.route("/api/wake", methods=["POST"])
def api_wake():
    player.stop_alarm()
    return jsonify({"status": "ok"})


def _scheduler_watchdog():
    import time
    while True:
        try:
            run_scheduler()
        except Exception:
            import traceback
            traceback.print_exc()
        time.sleep(1)

if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=_scheduler_watchdog, daemon=True)
    scheduler_thread.start()

    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)