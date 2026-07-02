"""
config/settings.py — Central configuration for JARVIS.
Edit this file to personalise your assistant.
"""

import os


class Settings:
    # ── Identity ──────────────────────────────────────────
    ASSISTANT_NAME   = "Jarvis"
    USER_NAME        = "Sir"          # ← Change to your name

    # ── Voice ─────────────────────────────────────────────
    VOICE_RATE       = 175
    VOICE_VOLUME     = 1.0
    VOICE_GENDER     = "male"         # "male" or "female"
    LISTEN_TIMEOUT   = 5
    PHRASE_LIMIT     = 10

    # ── Gmail (for reading emails) ─────────────────────────
    # Step 1: Enable 2-Step Verification on your Google Account
    # Step 2: Go to → myaccount.google.com/apppasswords
    # Step 3: Create an App Password → copy the 16-char code
    GMAIL_ADDRESS    = "your@gmail.com"       # ← Your Gmail
    GMAIL_APP_PASS   = "xxxx xxxx xxxx xxxx"  # ← App Password (not your real password)

    # ── News ──────────────────────────────────────────────
    # No API key needed — uses free BBC RSS feeds

    # ── Weather (optional) ────────────────────────────────
    WEATHER_API_KEY  = ""             # Free key from weatherapi.com
    DEFAULT_CITY     = "Delhi"        # ← Your city for weather

    # ── WhatsApp ──────────────────────────────────────────
    WHATSAPP_WAIT    = 10

    # ── Face Recognition ──────────────────────────────────
    # Set to True to enable face login at startup
    # First run: say "register my face" to register
    FACE_LOGIN       = True          # ← Set True after registering

    # ── Behaviour ─────────────────────────────────────────
    SHOW_SOURCES     = True
    TEXT_MODE        = False
    ALWAYS_SPEAK     = True

    # ── Paths ─────────────────────────────────────────────
    BASE_DIR         = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOG_DIR          = os.path.join(BASE_DIR, "logs")
    SKILLS_DIR       = os.path.join(BASE_DIR, "skills")
