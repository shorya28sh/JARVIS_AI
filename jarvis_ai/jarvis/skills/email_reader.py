"""
skills/email_reader.py — Read emails from Gmail via IMAP.

Setup (one time):
  1. Go to your Google Account → Security → 2-Step Verification → ON
  2. Then go to: myaccount.google.com/apppasswords
  3. Generate an App Password for "Mail"
  4. Put your Gmail + App Password in config/settings.py:
       GMAIL_ADDRESS  = "you@gmail.com"
       GMAIL_APP_PASS = "xxxx xxxx xxxx xxxx"

Commands:
  "read my emails"
  "check my inbox"
  "do I have new emails"
  "read latest emails"
"""

import imaplib
import email
from email.header import decode_header
import textwrap


def run(command: str, settings) -> dict:
    # Check credentials are configured
    gmail   = getattr(settings, "GMAIL_ADDRESS",  "")
    app_pass = getattr(settings, "GMAIL_APP_PASS", "")

    if not gmail or not app_pass or gmail == "your@gmail.com":
        return {
            "reply": (
                "To read emails, please add your Gmail credentials to config/settings.py. "
                "Set GMAIL_ADDRESS to your email and GMAIL_APP_PASS to your Gmail App Password. "
                "I've printed setup instructions in the terminal."
            )
        }

    how_many = 5  # Default: read 5 latest emails
    if "latest" in command or "recent" in command:
        how_many = 3

    try:
        # Connect to Gmail IMAP
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(gmail, app_pass)
        mail.select("inbox")

        # Search for unread or all emails
        if any(k in command for k in ["unread", "new", "naye"]):
            status, messages = mail.search(None, "UNSEEN")
        else:
            status, messages = mail.search(None, "ALL")

        email_ids = messages[0].split()
        if not email_ids:
            mail.logout()
            return {"reply": "Your inbox is empty or no new emails found."}

        # Read last N emails
        latest_ids = email_ids[-how_many:]
        results    = []

        for eid in reversed(latest_ids):
            _, msg_data = mail.fetch(eid, "(RFC822)")
            for part in msg_data:
                if isinstance(part, tuple):
                    msg    = email.message_from_bytes(part[1])
                    sender  = _decode_header(msg["From"])
                    subject = _decode_header(msg["Subject"])
                    body    = _get_body(msg)
                    results.append(f"From: {sender} | Subject: {subject} | {body[:100]}")

        mail.logout()

        if not results:
            return {"reply": "No emails to show."}

        summary = f"You have {len(email_ids)} emails. Here are the latest {len(results)}: "
        summary += " ... ".join(results)
        return {"reply": summary, "sources": [f"https://mail.google.com"]}

    except imaplib.IMAP4.error as e:
        return {
            "reply": (
                f"Could not connect to Gmail: {str(e)}. "
                "Please check your Gmail address and App Password in settings.py."
            )
        }
    except Exception as e:
        return {"reply": f"Email error: {str(e)}"}


def _decode_header(value: str) -> str:
    if not value:
        return "Unknown"
    try:
        decoded, enc = decode_header(value)[0]
        if isinstance(decoded, bytes):
            return decoded.decode(enc or "utf-8", errors="replace")
        return str(decoded)
    except Exception:
        return str(value)


def _get_body(msg) -> str:
    """Extract plain text body from email."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                    break
                except Exception:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode("utf-8", errors="replace")
        except Exception:
            pass
    return body.strip().replace("\n", " ")[:200]
