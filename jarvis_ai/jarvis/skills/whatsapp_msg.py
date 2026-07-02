"""
skills/whatsapp_msg.py — Send WhatsApp messages via pywhatkit.

Usage examples:
  "Send whatsapp message to 9876543210 hello how are you"
  "Send message on whatsapp to John hello"
"""

import datetime

try:
    import pywhatkit as kit
    PYWHATKIT_AVAILABLE = True
except ImportError:
    PYWHATKIT_AVAILABLE = False


# ── Saved contacts (add your contacts here!) ──────────────
CONTACTS = {
    "mom"    : "+91XXXXXXXXXX",
    "dad"    : "+91XXXXXXXXXX",
    "friend" : "+91XXXXXXXXXX",
    # Add more: "name" : "+91number"
}


def run(command: str, settings) -> dict:
    if not PYWHATKIT_AVAILABLE:
        return {
            "reply": (
                "pywhatkit is not installed. "
                "Run: pip install pywhatkit  to enable WhatsApp messaging."
            )
        }

    number, message = _parse(command, settings)

    if not number:
        return {
            "reply": (
                "I need a phone number or contact name. "
                "Say: 'Send WhatsApp message to 9876543210 your message here'"
            )
        }

    if not message:
        return {"reply": "What message would you like to send?"}

    # Schedule 2 minutes from now
    now  = datetime.datetime.now()
    hour = now.hour
    mins = now.minute + 2
    if mins >= 60:
        mins -= 60
        hour = (hour + 1) % 24

    try:
        kit.sendwhatmsg(number, message, hour, mins,
                        wait_time=settings.WHATSAPP_WAIT,
                        tab_close=True)
        return {
            "reply"  : (
                f"WhatsApp message scheduled to {number} at {hour}:{mins:02d}. "
                f"Message: '{message}'"
            ),
            "sources": ["https://web.whatsapp.com"],
        }
    except Exception as e:
        return {"reply": f"Failed to send WhatsApp message: {e}"}


# ── Helpers ───────────────────────────────────────────────

def _parse(command: str, settings):
    """Extract phone number (or contact name) and message from the command."""
    import re

    # Remove common prefixes
    for prefix in ["send whatsapp message to", "send message on whatsapp to",
                   "message bhejo", "whatsapp message", "send whatsapp",
                   "whatsapp ko", "send", "whatsapp"]:
        command = command.replace(prefix, "").strip()

    # Try to find a phone number
    phone_match = re.search(r'\+?\d{10,13}', command)
    if phone_match:
        number  = phone_match.group()
        if not number.startswith("+"):
            number = "+91" + number.lstrip("0")
        message = command.replace(phone_match.group(), "").strip()
        return number, message

    # Try contact name
    words = command.split()
    if words:
        name = words[0].lower()
        if name in CONTACTS:
            message = " ".join(words[1:]).strip()
            return CONTACTS[name], message

    return None, None
