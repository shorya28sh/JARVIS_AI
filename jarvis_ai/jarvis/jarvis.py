"""
J.A.R.V.I.S - AI Personal Assistant
Run: python jarvis.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.assistant  import JarvisAssistant
from core.voice      import VoiceEngine
from core.brain      import Brain
from config.settings import Settings


def main():
    print("=" * 55)
    print("   J.A.R.V.I.S  —  Initializing Systems...")
    print("=" * 55)

    settings = Settings()

    # Optional: Face Recognition Login
    if getattr(settings, "FACE_LOGIN", False):
        try:
            from skills.face_login import verify_at_startup
            if not verify_at_startup(settings):
                print("\n Lock Access denied. Exiting.")
                sys.exit(1)
        except ImportError:
            pass

    # Start JARVIS
    voice  = VoiceEngine(settings)
    brain  = Brain(settings)
    jarvis = JarvisAssistant(voice, brain, settings)

    jarvis.greet()
    jarvis.ask_mode()
    jarvis.run()


if __name__ == "__main__":
    main()
