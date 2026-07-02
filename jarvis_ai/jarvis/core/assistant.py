"""
core/assistant.py — Top-level JARVIS orchestrator.
"""

import datetime
import sys


class JarvisAssistant:
    def __init__(self, voice, brain, settings):
        self.voice    = voice
        self.brain    = brain
        self.settings = settings

    # ── Greeting ──────────────────────────────────────────

    def greet(self):
        hour = datetime.datetime.now().hour
        if   5  <= hour < 12: period = "Good morning"
        elif 12 <= hour < 17: period = "Good afternoon"
        elif 17 <= hour < 21: period = "Good evening"
        else:                 period = "Good night"

        self._banner()

        greeting = (
            f"{period}, {self.settings.USER_NAME}! "
            f"I am {self.settings.ASSISTANT_NAME}, your personal AI assistant. "
            f"All systems are online and ready."
        )
        print(f"\n🤖 {self.settings.ASSISTANT_NAME}: {greeting}")
        try:
            self.voice.tts.say(greeting)
            self.voice.tts.runAndWait()
        except Exception:
            pass

    # ── Ask mode ──────────────────────────────────────────

    def ask_mode(self):
        """Ask user: Voice Mode or Text Mode."""
        prompt = (
            "\n  How would you like to interact with me?\n"
            "  ┌─────────────────────────────────────────────┐\n"
            "  │  [1]  🎙️   Voice Mode                       │\n"
            "  │       Speak to me → I speak + show text     │\n"
            "  │                                             │\n"
            "  │  [2]  ⌨️   Text Mode                        │\n"
            "  │       Type to me → I reply in text only     │\n"
            "  └─────────────────────────────────────────────┘"
        )
        print(prompt)

        try:
            self.voice.tts.say(
                "Please choose your interaction mode. "
                "Press 1 for voice mode, or 2 for text mode."
            )
            self.voice.tts.runAndWait()
        except Exception:
            pass

        while True:
            try:
                choice = input("\n  Enter 1 or 2: ").strip()
            except (EOFError, KeyboardInterrupt):
                choice = "2"

            if choice == "1":
                if not self.voice.mic_ok():
                    print("\n  ⚠️  No microphone detected! Switching to Text Mode automatically.")
                    self._set_text_mode()
                else:
                    self._set_voice_mode()
                break
            elif choice == "2":
                self._set_text_mode()
                break
            else:
                print("  ❌  Please enter 1 or 2.")

    def _set_voice_mode(self):
        self.voice.set_mode("voice")
        confirm = (
            f"Voice mode activated! "
            f"I will listen for your commands and speak my replies. "
            f"Say 'exit' or 'bye' anytime to quit. "
            f"How can I help you, {self.settings.USER_NAME}?"
        )
        print(f"\n  ✅  Voice Mode ON — Mic is live!")
        print(f"\n🤖 {self.settings.ASSISTANT_NAME}: {confirm}")
        try:
            self.voice.tts.say(confirm)
            self.voice.tts.runAndWait()
        except Exception:
            pass

    def _set_text_mode(self):
        self.voice.set_mode("text")
        confirm = (
            f"Text mode activated! "
            f"Type your commands and I will reply in text. "
            f"Type 'exit' or 'bye' anytime to quit. "
            f"How can I help you, {self.settings.USER_NAME}?"
        )
        print(f"\n  ✅  Text Mode ON — Type your commands below.")
        print(f"\n🤖 {self.settings.ASSISTANT_NAME}: {confirm}")

    # ── Main loop ─────────────────────────────────────────

    def run(self):
        while True:
            try:
                command = self.voice.listen()

                if not command:
                    continue

                # Exit commands
                if command.strip() in ("exit", "quit", "bye", "goodbye",
                                       "band karo", "alvida"):
                    farewell = f"Goodbye, {self.settings.USER_NAME}! Have a great day!"
                    self.voice.speak(farewell)
                    sys.exit(0)

                # Switch mode mid-conversation
                if command in ("switch to text", "text mode", "text"):
                    self._set_text_mode()
                    continue
                if command in ("switch to voice", "voice mode", "voice"):
                    if self.voice.mic_ok():
                        self._set_voice_mode()
                    else:
                        self.voice.speak("Sorry, no microphone detected.")
                    continue

                # Process and respond
                result = self.brain.process(command)
                self._respond(result)

            except KeyboardInterrupt:
                self.voice.speak("Interrupted. Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"[JARVIS] Error: {e}")
                self.voice.speak("I hit an unexpected error. Please try again.")

    # ── Output ────────────────────────────────────────────

    def _respond(self, result: dict):
        reply   = result.get("reply",   "")
        sources = result.get("sources", [])

        self.voice.speak(reply)

        if self.settings.SHOW_SOURCES and sources:
            print("\n📚  Sources:")
            for i, src in enumerate(sources, 1):
                print(f"   {i}. {src}")
            print()

    # ── Banner ────────────────────────────────────────────

    def _banner(self):
        print()
        print("╔══════════════════════════════════════════════════════╗")
        print("║         J.A.R.V.I.S  —  Online & Ready              ║")
        print("╚══════════════════════════════════════════════════════╝")
        print(f"  Date : {datetime.datetime.now().strftime('%A, %d %B %Y')}")
        print(f"  Time : {datetime.datetime.now().strftime('%I:%M %p')}")
        print("  Tip  : Say 'switch to text' or 'switch to voice' anytime")
        print("─" * 56)
