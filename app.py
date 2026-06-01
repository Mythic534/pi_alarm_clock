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

from scheduler import get_next_alarm, stop_alarm

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
        raw = get_next_alarm()
        if raw is not None:
            if hasattr(raw, "next_run_time") and raw.next_run_time:
                # APScheduler Job object
                nrt   = raw.next_run_time
                label = raw.name or raw.id or "Alarm"
                alarm = {
                    "name": label,
                    "time": nrt.strftime("%H:%M"),
                    "day":  nrt.strftime("%a").upper(),
                    "date": nrt.strftime("%d %b %Y").upper(),
                }
            elif isinstance(raw, dict):
                # Caller already built a dict — use it directly
                alarm = raw
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
    """Touch event: silence a sounding alarm."""
    try:
        stop_alarm()
    except (ImportError, AttributeError):
        pass
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)