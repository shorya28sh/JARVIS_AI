# 🤖 J.A.R.V.I.S — Your Personal AI Assistant

> **J**ust **A** **R**ather **V**ery **I**ntelligent **S**ystem  
> Built in Python • Voice + Text • Expandable

---

## ✨ Features

| Feature | Command Example |
|---|---|
| 🌐 Open websites | *"Open YouTube"* / *"Open Gmail"* |
| 🎵 Play music | *"Play Arijit Singh"* / *"Play Lo-fi music"* |
| 💬 WhatsApp message | *"Send WhatsApp to 9876543210 Hello!"* |
| 🔍 Web search | *"What is black hole"* / *"Search Elon Musk"* |
| 🧮 Calculator | *"Calculate 25 times 4"* |
| 🕐 Date & Time | *"What time is it"* / *"Today's date"* |
| 😂 Jokes | *"Tell me a joke"* |
| 📸 Screenshot | *"Take a screenshot"* |
| 🔊 Volume control | *"Volume up"* / *"Volume down"* |
| 📝 Notes | *"Take note: buy groceries"* |
| 💤 Shutdown/Sleep | *"Shutdown"* / *"Sleep"* |

---

## 🚀 Quick Setup

### Step 1 — Install Python
Download Python 3.9+ from [python.org](https://python.org)

### Step 2 — Install PortAudio (for microphone)

**Windows:**
```
pip install pipwin
pipwin install pyaudio
```

**Ubuntu / Debian:**
```bash
sudo apt update
sudo apt install portaudio19-dev python3-pyaudio ffmpeg
```

**macOS:**
```bash
brew install portaudio
```

### Step 3 — Install all packages
```bash
pip install -r requirements.txt
```

### Step 4 — Run JARVIS!
```bash
python jarvis.py
```

---

## ⚙️ Configuration (`config/settings.py`)

| Setting | What it does |
|---|---|
| `USER_NAME` | Change "Sir" to your name |
| `VOICE_GENDER` | `"male"` or `"female"` |
| `VOICE_RATE` | Speech speed (default 175) |
| `TEXT_MODE` | `True` = type commands (no mic needed) |
| `SHOW_SOURCES` | Show where info was found |
| `WHATSAPP_WAIT` | Seconds before WhatsApp message sends |

---

## 📁 Project Structure

```
jarvis/
├── jarvis.py              ← Main entry point (run this!)
├── requirements.txt       ← All dependencies
├── README.md
│
├── config/
│   └── settings.py        ← All configuration here
│
├── core/
│   ├── assistant.py       ← Greeting + main loop
│   ├── voice.py           ← Mic + speaker engine
│   └── brain.py           ← Command router ← ADD SKILLS HERE
│
├── skills/                ← Each skill is one file
│   ├── web_open.py        ← Open websites
│   ├── music.py           ← Play music
│   ├── whatsapp_msg.py    ← Send WhatsApp
│   ├── web_search.py      ← Search the web
│   ├── calculator.py      ← Maths
│   ├── datetime_skill.py  ← Date & time
│   ├── jokes.py           ← Jokes
│   ├── system_ctrl.py     ← Volume, screenshot, shutdown
│   └── notes.py           ← Save & read notes
│
└── logs/                  ← Screenshots + notes saved here
```

---

## ➕ How to Add a New Skill (Future Improvements)

**1. Create the skill file** `skills/my_skill.py`:
```python
def run(command: str, settings) -> dict:
    # Your logic here
    return {
        "reply"  : "Done!",
        "sources": ["https://example.com"]
    }
```

**2. Add triggers in** `core/brain.py`:
```python
from skills import my_skill

SKILL_MAP = [
    # ...existing skills...
    (["my trigger phrase"], my_skill),
]
```

That's it! JARVIS will automatically recognise the new skill.

---

## 💡 Improvement Ideas (Tell Claude these!)

- [ ] Add weather skill (needs free API key from weatherapi.com)
- [ ] Add email reading via Gmail API
- [ ] Add news briefing
- [ ] Add reminder / alarm
- [ ] Add smart home control
- [ ] Add Hindi language support (full)
- [ ] Add face recognition login
- [ ] Add ChatGPT / Gemini for smarter answers

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| No microphone | Set `TEXT_MODE = True` in settings.py |
| pyaudio install fails | Follow OS-specific steps in Step 2 |
| WhatsApp not sending | Make sure Chrome is installed + logged in |
| TTS not speaking | Check speakers; try `ALWAYS_SPEAK = False` |

---

## 📞 Ask for Improvements

Just tell Claude:  
*"Add a weather skill to my JARVIS"*  
*"Make JARVIS remember my preferences"*  
*"Add Hindi voice support"*

The modular design means each improvement is just one new file! 🚀
