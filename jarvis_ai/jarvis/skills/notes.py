"""
skills/notes.py — Save and retrieve personal notes.

Commands:
  "Take note / remember / write down: buy groceries tomorrow"
  "Read my notes / what did I note"
"""

import os
import datetime


def run(command: str, settings) -> dict:
    notes_file = os.path.join(settings.LOG_DIR, "notes.txt")
    os.makedirs(settings.LOG_DIR, exist_ok=True)

    # Read notes
    if any(k in command for k in ["read", "show", "what did i note",
                                   "meri notes", "notes dikhao"]):
        return _read_notes(notes_file)

    # Save a note
    note = _extract_note(command)
    if not note:
        return {"reply": "What would you like me to note down?"}
    return _save_note(note, notes_file)


def _save_note(note: str, path: str) -> dict:
    ts = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {note}\n")
    return {"reply": f"Got it! I've noted: '{note}'"}


def _read_notes(path: str) -> dict:
    if not os.path.exists(path):
        return {"reply": "You have no saved notes yet."}
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if not lines:
        return {"reply": "Your notes are empty."}
    recent = lines[-5:]   # Last 5 notes
    formatted = " | ".join(l.strip() for l in recent)
    return {"reply": f"Here are your recent notes: {formatted}"}


def _extract_note(command: str) -> str:
    for kw in ["take note", "save note", "note karo", "remember",
               "write down", "note down", "note that"]:
        command = command.replace(kw, "").strip()
    # Remove leading colon or dash
    return command.lstrip(":- ").strip()
