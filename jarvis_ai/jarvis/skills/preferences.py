"""
skills/preferences.py — Remember and recall user preferences.

Commands:
  "remember I like jazz music"
  "remember my city is Delhi"
  "remember I wake up at 7am"
  "what do you know about me"
  "forget my city"
"""

import json
import os


def _prefs_file(settings) -> str:
    os.makedirs(settings.LOG_DIR, exist_ok=True)
    return os.path.join(settings.LOG_DIR, "preferences.json")


def _load(settings) -> dict:
    path = _prefs_file(settings)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _save(prefs: dict, settings):
    with open(_prefs_file(settings), "w", encoding="utf-8") as f:
        json.dump(prefs, f, indent=2)


def run(command: str, settings) -> dict:
    prefs = _load(settings)

    # ── Forget a preference ───────────────────────────────
    if "forget" in command:
        key = command.replace("forget", "").replace("my", "").strip()
        if key in prefs:
            del prefs[key]
            _save(prefs, settings)
            return {"reply": f"Got it! I've forgotten your {key}."}
        return {"reply": f"I don't have anything saved for '{key}'."}

    # ── Recall all preferences ────────────────────────────
    if any(k in command for k in ["what do you know", "my preferences",
                                   "what do you remember", "recall"]):
        if not prefs:
            return {"reply": "I don't have any preferences saved yet. Tell me things like: 'remember I like jazz music'."}
        lines = [f"{k}: {v}" for k, v in prefs.items()]
        summary = ", ".join(lines)
        return {"reply": f"Here's what I know about you — {summary}."}

    # ── Save a preference ─────────────────────────────────
    text = command
    for kw in ["remember", "my", "i like", "i love", "i prefer",
               "i am", "i wake up", "i live", "save that"]:
        text = text.replace(kw, "")
    text = text.strip()

    if not text:
        return {"reply": "What would you like me to remember?"}

    # Try to parse "key is value"
    if " is " in text:
        parts = text.split(" is ", 1)
        key, value = parts[0].strip(), parts[1].strip()
    elif " at " in text:
        parts = text.split(" at ", 1)
        key, value = parts[0].strip(), "at " + parts[1].strip()
    else:
        key   = "note_" + str(len(prefs) + 1)
        value = text

    prefs[key] = value
    _save(prefs, settings)
    return {"reply": f"Got it! I'll remember that your {key} is {value}."}


def get_preferences(settings) -> dict:
    """Called by other skills to read saved preferences."""
    return _load(settings)
