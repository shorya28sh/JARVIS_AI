"""
skills/news.py — Fetch and read top news headlines.

Commands:
  "read the news"
  "morning briefing"
  "latest news"
  "technology news"
  "sports news"
  "news briefing"

Uses RSS feeds — no API key needed!
"""

import urllib.request
import xml.etree.ElementTree as ET
import re


# Free RSS feeds — no API key needed
FEEDS = {
    "top"         : "https://feeds.bbci.co.uk/news/rss.xml",
    "technology"  : "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "sports"      : "https://feeds.bbci.co.uk/news/sport/rss.xml",
    "business"    : "https://feeds.bbci.co.uk/news/business/rss.xml",
    "india"       : "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml",
    "world"       : "https://feeds.bbci.co.uk/news/world/rss.xml",
    "science"     : "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "health"      : "https://feeds.bbci.co.uk/news/health/rss.xml",
}


def run(command: str, settings) -> dict:
    # Pick the right feed based on command
    feed_url  = FEEDS["top"]
    category  = "top"

    for cat, url in FEEDS.items():
        if cat in command:
            feed_url = url
            category = cat
            break

    # How many headlines
    count = 5
    if "brief" in command or "morning" in command:
        count = 7

    try:
        headlines, sources = _fetch_headlines(feed_url, count)
    except Exception as e:
        return {"reply": f"Sorry, I couldn't fetch the news right now: {str(e)}"}

    if not headlines:
        return {"reply": "No news headlines found at the moment."}

    intro  = f"Here are the top {len(headlines)} {category} news headlines. "
    body   = " ... ".join(
        [f"Headline {i+1}: {h}" for i, h in enumerate(headlines)]
    )
    return {
        "reply"  : intro + body,
        "sources": sources,
    }


def _fetch_headlines(url: str, count: int):
    """Fetch and parse RSS feed, return list of headlines and source URLs."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=8) as resp:
        content = resp.read()

    root      = ET.fromstring(content)
    headlines = []
    sources   = []

    for item in root.iter("item"):
        title = item.findtext("title") or ""
        link  = item.findtext("link")  or ""
        title = _clean(title)
        if title:
            headlines.append(title)
            sources.append(link)
        if len(headlines) >= count:
            break

    return headlines, sources


def _clean(text: str) -> str:
    """Strip HTML tags and extra whitespace."""
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()
