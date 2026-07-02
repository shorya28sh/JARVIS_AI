"""
skills/datetime_skill.py — Current date, time, and day.
"""

import datetime


def run(command: str, settings) -> dict:
    now  = datetime.datetime.now()
    time = now.strftime("%I:%M %p")
    date = now.strftime("%A, %d %B %Y")

    if any(k in command for k in ["time", "baja", "kitna baja", "samay"]):
        return {"reply": f"The current time is {time}."}

    if any(k in command for k in ["date", "tarikh", "aaj"]):
        return {"reply": f"Today is {date}."}

    return {"reply": f"It is {time} on {date}."}
