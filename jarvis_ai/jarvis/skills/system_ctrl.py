"""
skills/system_ctrl.py — Control PC: volume, screenshot, shutdown, etc.
"""

import os
import platform
import subprocess
import datetime

try:
    from pynput.keyboard import Key, Controller
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False


SYSTEM = platform.system()   # "Windows", "Linux", "Darwin"


def run(command: str, settings) -> dict:

    # ── Screenshot ────────────────────────────────────────
    if "screenshot" in command:
        return _screenshot(settings)

    # ── Volume ────────────────────────────────────────────
    if "volume up" in command or "aawaz badho" in command:
        return _volume("up")

    if "volume down" in command or "aawaz kam" in command:
        return _volume("down")

    if "mute" in command or "chup" in command:
        return _volume("mute")

    # ── Power ─────────────────────────────────────────────
    if "shutdown" in command or "band karo" in command:
        return _power("shutdown")

    if "restart" in command or "reboot" in command:
        return _power("restart")

    if "sleep" in command or "so jao" in command:
        return _power("sleep")

    if "lock" in command:
        return _power("lock")

    return {"reply": "System command not recognised. Try: volume up, volume down, screenshot, shutdown."}


# ── Helpers ───────────────────────────────────────────────

def _screenshot(settings):
    try:
        import pyautogui
        ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(settings.LOG_DIR, f"screenshot_{ts}.png")
        os.makedirs(settings.LOG_DIR, exist_ok=True)
        pyautogui.screenshot(path)
        return {
            "reply"  : f"Screenshot saved as screenshot_{ts}.png",
            "sources": [path],
        }
    except ImportError:
        return {"reply": "pyautogui is not installed. Run: pip install pyautogui"}
    except Exception as e:
        return {"reply": f"Screenshot failed: {e}"}


def _volume(action: str) -> dict:
    try:
        if SYSTEM == "Windows":
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            # Simple keyboard approach as fallback
            _press_media_key(action)
        elif SYSTEM == "Darwin":   # macOS
            if action == "up":
                os.system("osascript -e 'set volume output volume (output volume of (get volume settings) + 10)'")
            elif action == "down":
                os.system("osascript -e 'set volume output volume (output volume of (get volume settings) - 10)'")
            elif action == "mute":
                os.system("osascript -e 'set volume output muted true'")
        elif SYSTEM == "Linux":
            if action == "up":
                os.system("amixer -D pulse sset Master 10%+")
            elif action == "down":
                os.system("amixer -D pulse sset Master 10%-")
            elif action == "mute":
                os.system("amixer -D pulse sset Master toggle")

        labels = {"up": "Volume increased", "down": "Volume decreased", "mute": "Muted"}
        return {"reply": labels.get(action, "Volume adjusted")}
    except Exception as e:
        return {"reply": f"Could not change volume: {e}"}


def _press_media_key(action: str):
    if PYNPUT_AVAILABLE:
        kb = Controller()
        key_map = {
            "up"  : Key.media_volume_up,
            "down": Key.media_volume_down,
            "mute": Key.media_volume_mute,
        }
        if action in key_map:
            kb.press(key_map[action])
            kb.release(key_map[action])


def _power(action: str) -> dict:
    cmds = {
        "Windows": {
            "shutdown": "shutdown /s /t 5",
            "restart" : "shutdown /r /t 5",
            "sleep"   : "rundll32.exe powrprof.dll,SetSuspendState 0,1,0",
            "lock"    : "rundll32.exe user32.dll,LockWorkStation",
        },
        "Linux": {
            "shutdown": "systemctl poweroff",
            "restart" : "systemctl reboot",
            "sleep"   : "systemctl suspend",
            "lock"    : "loginctl lock-session",
        },
        "Darwin": {
            "shutdown": "osascript -e 'tell app \"System Events\" to shut down'",
            "restart" : "osascript -e 'tell app \"System Events\" to restart'",
            "sleep"   : "pmset sleepnow",
            "lock"    : "pmset displaysleepnow",
        },
    }
    cmd = cmds.get(SYSTEM, {}).get(action)
    if cmd:
        os.system(cmd)
        return {"reply": f"Executing {action}…"}
    return {"reply": f"{action.capitalize()} is not supported on your OS."}
