"""
core/voice.py — Speech Recognition + Text-to-Speech engine.
"""

import pyttsx3
import speech_recognition as sr
import sys


class VoiceEngine:
    """Handles all voice I/O for JARVIS."""

    MODE_VOICE = "voice"
    MODE_TEXT  = "text"

    def __init__(self, settings):
        self.settings = settings
        self.mode     = None       # Set after user picks mode
        self._init_tts()
        self._init_stt()

    # ── Text-to-Speech ────────────────────────────────────

    def _init_tts(self):
        try:
            self.tts = pyttsx3.init()
            self.tts.setProperty("rate",   self.settings.VOICE_RATE)
            self.tts.setProperty("volume", self.settings.VOICE_VOLUME)

            voices = self.tts.getProperty("voices")
            chosen = None
            for v in voices:
                name = (v.name or "").lower()
                if self.settings.VOICE_GENDER == "male"   and "male"   in name:
                    chosen = v.id; break
                if self.settings.VOICE_GENDER == "female" and "female" in name:
                    chosen = v.id; break
            if chosen:
                self.tts.setProperty("voice", chosen)

            self.tts_ready = True
        except Exception as e:
            print(f"[Voice] TTS init failed: {e}")
            self.tts_ready = False

    def speak(self, text: str, print_text: bool = True):
        """Speak aloud (voice mode) or print only (text mode)."""
        if print_text:
            print(f"\n🤖 {self.settings.ASSISTANT_NAME}: {text}")

        # Only speak out loud in voice mode
        if self.mode == self.MODE_VOICE and self.tts_ready:
            try:
                self.tts.say(text)
                self.tts.runAndWait()
            except Exception as e:
                print(f"[Voice] TTS error: {e}")

    # ── Speech-to-Text ────────────────────────────────────

    def _init_stt(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold        = 300
        self.recognizer.dynamic_energy_threshold = True
        self._mic_available = True
        try:
            with sr.Microphone() as src:
                self.recognizer.adjust_for_ambient_noise(src, duration=1)
        except Exception:
            self._mic_available = False
            print("[Voice] No microphone detected — text input only.")

    # ── Listen ────────────────────────────────────────────

    def listen(self) -> str:
        """Route to mic or keyboard depending on current mode."""
        if self.mode == self.MODE_TEXT or not self._mic_available:
            return self._text_input()
        return self._voice_input()

    def _voice_input(self) -> str:
        print("\n🎙️  Mic ON — speak your command…")
        try:
            with sr.Microphone() as src:
                audio = self.recognizer.listen(
                    src,
                    timeout=self.settings.LISTEN_TIMEOUT,
                    phrase_time_limit=self.settings.PHRASE_LIMIT,
                )
            text = self.recognizer.recognize_google(audio)
            print(f"👤 You said: {text}")
            return text.lower().strip()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Please repeat.")
            return ""
        except sr.RequestError as e:
            print(f"[Voice] STT error: {e}")
            return self._text_input()

    def _text_input(self) -> str:
        try:
            return input("\n⌨️  You: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return "exit"

    # ── Mode control ──────────────────────────────────────

    def set_mode(self, mode: str):
        """Set interaction mode: 'voice' or 'text'."""
        self.mode = mode

    def mic_ok(self) -> bool:
        """Return True if a microphone is available."""
        return self._mic_available
