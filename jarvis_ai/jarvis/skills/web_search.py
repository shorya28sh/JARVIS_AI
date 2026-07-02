"""
skills/web_search.py — Search the web and return a clean summary.

Sources used (in order):
  1. Wikipedia  — for factual "what is / who is" queries
  2. DuckDuckGo — for everything else (no API key needed)
"""

import webbrowser
import urllib.parse

try:
    import wikipedia
    WIKIPEDIA_AVAILABLE = True
except ImportError:
    WIKIPEDIA_AVAILABLE = False

try:
    from duckduckgo_search import DDGS
    DDG_AVAILABLE = True
except ImportError:
    DDG_AVAILABLE = False


def run(command: str, settings) -> dict:
    query = _clean_query(command)

    if not query:
        return {"reply": "What would you like me to search for?"}

    sources = []
    reply   = ""

    # ── 1. Wikipedia for factual queries ──────────────────
    if WIKIPEDIA_AVAILABLE and _is_factual(command):
        try:
            wikipedia.set_lang("en")
            summary = wikipedia.summary(query, sentences=3, auto_suggest=True)
            page    = wikipedia.page(query, auto_suggest=True)
            sources.append(page.url)
            reply = summary
        except wikipedia.exceptions.DisambiguationError as e:
            # Take first option
            try:
                summary = wikipedia.summary(e.options[0], sentences=3)
                sources.append(f"https://en.wikipedia.org/wiki/{urllib.parse.quote(e.options[0])}")
                reply = summary
            except Exception:
                pass
        except Exception:
            pass  # fall through to DuckDuckGo

    # ── 2. DuckDuckGo for general queries ─────────────────
    if not reply and DDG_AVAILABLE:
        try:
            with DDGS() as ddg:
                results = list(ddg.text(query, max_results=3))
            if results:
                # Build a clean multi-source summary
                parts = []
                for r in results:
                    parts.append(r.get("body", ""))
                    sources.append(r.get("href", ""))
                reply = " ".join(parts[:2])  # Use top-2 snippets
        except Exception as e:
            pass

    # ── 3. Fallback — open browser ────────────────────────
    if not reply:
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        webbrowser.open(url)
        return {
            "reply"  : f"I couldn't find a direct answer. I've opened Google for '{query}'.",
            "sources": [url],
        }

    # Trim to a reasonable length
    if len(reply) > 500:
        reply = reply[:497] + "…"

    return {
        "reply"  : reply,
        "sources": [s for s in sources if s],
    }


# ── Helpers ───────────────────────────────────────────────

def _clean_query(command: str) -> str:
    for kw in ["search", "find", "look up", "tell me about", "what is",
               "who is", "explain", "dhundo", "batao", "kya hai",
               "search for", "google"]:
        command = command.replace(kw, "").strip()
    return command.strip()


def _is_factual(command: str) -> bool:
    factual_kw = ["what is", "who is", "define", "explain",
                  "tell me about", "kya hai", "kaun hai", "batao"]
    return any(kw in command for kw in factual_kw)
