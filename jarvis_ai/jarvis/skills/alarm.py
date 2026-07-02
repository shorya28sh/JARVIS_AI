"""
skills/alarm.py — Set alarms and reminders.

Commands:
  "set alarm at 7:30 am"
  "remind me at 6pm to drink water"
  "set reminder for 10:00 to call mom"
  "show my alarms"
  "cancel alarm"

Alarms run in a background thread and speak/print when triggered.
"""

import threading
import datetime
import time
import re
import json
import os


# Shared list of active alarms (in-memory + saved to file)
_alarms = []
_lock   = threading.Lock()


def _alarms_file(settings) -> str:
    os.makedirs(settings.LOG_DIR, exist_ok=True)
    return os.path.join(settings.LOG_DIR, "alarms.json")


def _save_alarms(settings):
    data = [
        {"time": a["time"].strftime("%H:%M"), "label": a["label"]}
        for a in _alarms if not a.get("done")
    ]
    with open(_alarms_file(settings), "w") as f:
        json.dump(data, f, indent=2)


def run(command: str, settings) -> dict:
    global _alarms

    # ── Show alarms ───────────────────────────────────────
    if any(k in command for k in ["show", "list", "my alarms", "what alarms"]):
        with _lock:
            active = [a for a in _alarms if not a.get("done")]
        if not active:
            return {"reply": "You have no active alarms."}
        lines = [f"{a['time'].strftime('%I:%M %p')} — {a['label']}" for a in active]
        return {"reply": "Your alarms: " + ", ".join(lines)}

    # ── Cancel alarm ──────────────────────────────────────
    if "cancel" in command or "delete" in command or "remove" in command:
        with _lock:
            _alarms.clear()
        _save_alarms(settings)
        return {"reply": "All alarms cancelled."}

    # ── Parse time & label ────────────────────────────────
    alarm_time, label = _parse(command)
    if not alarm_time:
        return {"reply": "I couldn't understand the time. Try: 'Set alarm at 7:30 am' or 'Remind me at 6pm to drink water'."}

    # Schedule the alarm in a background thread
    alarm_entry = {"time": alarm_time, "label": label, "done": False}
    with _lock:
        _alarms.append(alarm_entry)
    _save_alarms(settings)

    t = threading.Thread(target=_alarm_worker,
                         args=(alarm_entry, settings), daemon=True)
    t.start()

    time_str = alarm_time.strftime("%I:%M %p")
    return {"reply": f"Alarm set for {time_str}! I'll remind you: '{label}'."}


def _alarm_worker(alarm: dict, settings):
    """Background thread — waits until alarm time, then fires."""
    while True:
        now = datetime.datetime.now()
        if now >= alarm["time"] and not alarm["done"]:
            alarm["done"] = True
            _fire(alarm, settings)
            break
        time.sleep(20)  # Check every 20 seconds


def _fire(alarm: dict, settings):
    """Trigger the alarm — print + speak."""
    msg = f"⏰  ALARM! {alarm['label']}"
    print(f"\n\n{'='*50}")
    print(f"  {msg}")
    print(f"{'='*50}\n")
    try:
        import pyttsx3
        tts = pyttsx3.init()
        tts.say(f"Attention! {alarm['label']}")
        tts.runAndWait()
    except Exception:
        pass


def _parse(command: str):
    """Extract time and label from the command string."""
    now   = datetime.datetime.now()
    label = "Reminder"

    # Extract label after 'to'
    to_match = re.search(r'\bto\b (.+)', command)
    if to_match:
        label = to_match.group(1).strip()
        command = command[:to_match.start()]

    # Try HH:MM am/pm
    match = re.search(r'(\d{1,2}):(\d{2})\s*(am|pm)?', command, re.IGNORECASE)
    if match:
        hour, minute = int(match.group(1)), int(match.group(2))
        period = (match.group(3) or "").lower()
        if period == "pm" and hour != 12:
            hour += 12
        if period == "am" and hour == 12:
            hour = 0
        alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if alarm_time <= now:
            alarm_time += datetime.timedelta(days=1)
        return alarm_time, label

    # Try H am/pm  e.g. "6pm", "7 am"
    match = re.search(r'(\d{1,2})\s*(am|pm)', command, re.IGNORECASE)
    if match:
        hour   = int(match.group(1))
        period = match.group(2).lower()
        if period == "pm" and hour != 12:
            hour += 12
        if period == "am" and hour == 12:
            hour = 0
        alarm_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
        if alarm_time <= now:
            alarm_time += datetime.timedelta(days=1)
        return alarm_time, label

    # Try "in X minutes"
    match = re.search(r'in (\d+) minute', command)
    if match:
        mins       = int(match.group(1))
        alarm_time = now + datetime.timedelta(minutes=mins)
        return alarm_time, label

    # Try "in X hours"
    match = re.search(r'in (\d+) hour', command)
    if match:
        hours      = int(match.group(1))
        alarm_time = now + datetime.timedelta(hours=hours)
        return alarm_time, label

    return None, label
