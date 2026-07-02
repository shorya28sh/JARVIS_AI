"""
core/brain.py — JARVIS command interpreter & skill router.

HOW TO ADD A NEW SKILL:
  1. Create   skills/my_skill.py  with a function  run(query, settings)
  2. Add a new entry to  SKILL_MAP  below.
"""

from skills import (
    web_open, music, whatsapp_msg, web_search,
    calculator, datetime_skill, jokes, system_ctrl, notes,
    preferences, alarm, email_reader, news,
)

# Lazy import face_login to avoid crash if deepface/opencv not installed
try:
    from skills import face_login as face_login_skill
    FACE_AVAILABLE = True
except Exception:
    face_login_skill = None
    FACE_AVAILABLE   = False


# ── Skill routing map ─────────────────────────────────────
SKILL_MAP = [
    # --- Web & Apps ---
    (["open youtube", "youtube kholo"],                          web_open),
    (["open google", "google kholo"],                            web_open),
    (["open facebook", "facebook kholo"],                        web_open),
    (["open instagram", "instagram kholo"],                      web_open),
    (["open twitter", "twitter kholo"],                          web_open),
    (["open github", "github kholo"],                            web_open),
    (["open whatsapp", "whatsapp kholo"],                        web_open),
    (["open netflix", "netflix kholo"],                          web_open),
    (["open gmail", "gmail kholo"],                              web_open),

    # --- Music ---
    (["play music", "gaana bajao", "play song", "play"],         music),

    # --- WhatsApp ---
    (["send whatsapp", "whatsapp message", "message bhejo",
      "send message on whatsapp"],                               whatsapp_msg),

    # --- Alarms & Reminders ---
    (["set alarm", "alarm set", "remind me", "set reminder",
      "alarm lagao", "reminder", "wake me",
      "show alarms", "cancel alarm"],                            alarm),

    # --- Email ---
    (["read my email", "check email", "check inbox",
      "new email", "unread email", "do i have email",
      "latest email"],                                           email_reader),

    # --- News ---
    (["news", "headlines", "briefing", "morning briefing",
      "latest news", "khabar", "samachar",
      "technology news", "sports news", "india news"],           news),

    # --- Preferences ---
    (["remember", "save my", "my preference",
      "what do you know", "what do you remember",
      "recall", "forget my", "i like", "i love",
      "i prefer"],                                               preferences),

    # --- Face Recognition ---
    (["register my face", "enroll face", "train face",
      "verify face", "face login",
      "face recognition"],                                       face_login_skill),

    # --- Calculator ---
    (["calculate", "compute", "how much is",
      "hisab karo"],                                             calculator),

    # --- Date / Time ---
    (["time", "date", "day", "kitna baja",
      "aaj ki tarikh"],                                          datetime_skill),

    # --- Jokes ---
    (["joke", "joke sunao", "make me laugh", "funny"],           jokes),

    # --- System ---
    (["shutdown", "restart", "sleep", "lock",
      "volume up", "volume down", "screenshot"],                 system_ctrl),

    # --- Notes ---
    (["take note", "save note", "note karo",
      "write down"],                                             notes),

    # --- Search (catch-all) ---
    (["search", "find", "look up", "tell me about",
      "what is", "who is", "explain",
      "dhundo", "batao", "kya hai"],                             web_search),
]


class Brain:
    def __init__(self, settings):
        self.settings = settings

    def process(self, command: str) -> dict:
        command = command.lower().strip()

        if not command:
            return self._empty()

        for triggers, skill_module in SKILL_MAP:
            # Skip if skill failed to import (e.g. face_login without deepface)
            if skill_module is None:
                continue
            for trigger in triggers:
                if trigger in command:
                    try:
                        result = skill_module.run(command, self.settings)
                        return self._normalize(result, skill_module.__name__)
                    except Exception as e:
                        return {
                            "reply"  : f"Sorry, I hit an error: {e}",
                            "sources": [],
                            "skill"  : str(skill_module),
                        }

        # Fallback — general web search
        try:
            result = web_search.run(command, self.settings)
            return self._normalize(result, "web_search")
        except Exception:
            return {
                "reply"  : "I'm not sure how to handle that. Try rephrasing!",
                "sources": [],
                "skill"  : "unknown",
            }

    def _normalize(self, result, skill_name: str) -> dict:
        if isinstance(result, str):
            return {"reply": result, "sources": [], "skill": skill_name}
        result.setdefault("sources", [])
        result.setdefault("skill",   skill_name)
        return result

    def _empty(self) -> dict:
        return {
            "reply"  : "I didn't hear a command. Please try again.",
            "sources": [],
            "skill"  : "none",
        }
