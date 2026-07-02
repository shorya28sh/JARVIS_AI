"""
skills/music.py — Play music via YouTube (pywhatkit) or local files.
"""

import urllib.parse
import webbrowser

try:
    import pywhatkit as kit
    PYWHATKIT_AVAILABLE = True
except ImportError:
    PYWHATKIT_AVAILABLE = False


def run(command: str, settings) -> dict:
    # Extract song/artist name from command
    song = _extract_song(command)

    if PYWHATKIT_AVAILABLE:
        try:
            kit.playonyt(song)
            return {
                "reply"  : f"Playing '{song}' on YouTube for you!",
                "sources": [f"https://www.youtube.com/results?search_query={urllib.parse.quote(song)}"],
            }
        except Exception as e:
            pass  # fall through to manual search

    # Fallback: open YouTube search in browser
    query = urllib.parse.quote(song)
    url   = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    return {
        "reply"  : f"Searching YouTube for '{song}'!",
        "sources": [url],
    }


def _extract_song(command: str) -> str:
    for kw in ["play", "music", "gaana", "bajao", "song", "gana"]:
        command = command.replace(kw, "")
    song = command.strip()
    return song if song else "top hindi songs 2024"
