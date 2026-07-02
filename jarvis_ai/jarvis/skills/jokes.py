"""
skills/jokes.py — Fetches a random joke via pyjokes or an API.
"""

import random

try:
    import pyjokes
    PYJOKES_AVAILABLE = True
except ImportError:
    PYJOKES_AVAILABLE = False


FALLBACK_JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads.",
    "Why did the programmer quit? Because he didn't get arrays.",
    "How many programmers does it take to change a light bulb? None — that's a hardware problem.",
    "Why do Java developers wear glasses? Because they don't C#.",
    "I would tell you a UDP joke, but you might not get it.",
    "A SQL query walks into a bar, walks up to two tables and asks: 'Can I join you?'",
    "There are 10 types of people: those who understand binary and those who don't.",
]


def run(command: str, settings) -> dict:
    if PYJOKES_AVAILABLE:
        try:
            joke = pyjokes.get_joke(language="en", category="all")
            return {"reply": joke}
        except Exception:
            pass
    return {"reply": random.choice(FALLBACK_JOKES)}
