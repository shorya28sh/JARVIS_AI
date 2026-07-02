"""
skills/web_open.py — Open websites & apps in the browser.

Add more sites to SITE_MAP as needed!
"""

import webbrowser

SITE_MAP = {
    "youtube"   : "https://www.youtube.com",
    "google"    : "https://www.google.com",
    "facebook"  : "https://www.facebook.com",
    "instagram" : "https://www.instagram.com",
    "twitter"   : "https://www.twitter.com",
    "github"    : "https://www.github.com",
    "whatsapp"  : "https://web.whatsapp.com",
    "netflix"   : "https://www.netflix.com",
    "gmail"     : "https://mail.google.com",
    "amazon"    : "https://www.amazon.in",
    "flipkart"  : "https://www.flipkart.com",
    "linkedin"  : "https://www.linkedin.com",
    "reddit"    : "https://www.reddit.com",
    "spotify"   : "https://open.spotify.com",
    "maps"      : "https://maps.google.com",
    "news"      : "https://news.google.com",
    "wikipedia" : "https://www.wikipedia.org",
}


def run(command: str, settings) -> dict:
    for site_name, url in SITE_MAP.items():
        if site_name in command:
            webbrowser.open(url)
            return {
                "reply"  : f"Opening {site_name.capitalize()} for you, {settings.USER_NAME}!",
                "sources": [url],
            }

    # Generic open — try to extract the site name
    words = command.replace("open", "").replace("kholo", "").split()
    if words:
        site = words[0].strip()
        url  = f"https://www.{site}.com"
        webbrowser.open(url)
        return {
            "reply"  : f"Trying to open {site}…",
            "sources": [url],
        }

    return {"reply": "Which website would you like me to open?"}
