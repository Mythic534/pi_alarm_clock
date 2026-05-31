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

# ── Import your scheduler ────────────────────────────────────────────────────
from scheduler import get_next_alarm  # adjust if your module path differs

class _StatusFilter(logging.Filter):
    """Filter out log spam."""
    def filter(self, record):
        return '/api/status' not in record.getMessage()

logging.getLogger('werkzeug').addFilter(_StatusFilter())

app = Flask(__name__)

# ── Backlight ────────────────────────────────────────────────────────────────
# Pi Touch Display 2 uses an I²C LP855x backlight controller.
# Check   ls /sys/class/backlight/   on your Pi; the path is often:
#   /sys/class/backlight/10-0045/brightness   (Display 2)
#   /sys/class/backlight/rpi_backlight/brightness  (original display)
BACKLIGHT_PATH   = "/sys/class/backlight/10-0045/brightness"
BACKLIGHT_BRIGHT = 200   # 0–255, normal brightness
BACKLIGHT_DIM    = 12    # dim-to level after inactivity


def _set_backlight(level: int) -> None:
    """Write brightness to sysfs. Silently skips on non-Pi hardware."""
    try:
        with open(BACKLIGHT_PATH, "w") as fh:
            fh.write(str(max(0, min(255, level))))
    except OSError:
        pass


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template(
        "clock.html",
        dim_after_seconds=30,   # seconds of inactivity before screen dims
    )


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
    """Touch event: restore backlight and silence a sounding alarm."""
    _set_backlight(BACKLIGHT_BRIGHT)
    try:
        from scheduler import stop_alarm   # implement in scheduler.py if needed
        stop_alarm()
    except (ImportError, AttributeError):
        pass
    return jsonify({"status": "ok"})


@app.route("/api/dim", methods=["POST"])
def api_dim():
    """Inactivity timeout: reduce backlight."""
    _set_backlight(BACKLIGHT_DIM)
    return jsonify({"status": "ok"})


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    _set_backlight(BACKLIGHT_BRIGHT)
    # threaded=True so polling requests don't block each other
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
