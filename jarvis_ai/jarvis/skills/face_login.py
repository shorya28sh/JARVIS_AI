"""
skills/face_login.py — Face recognition login using DeepFace.
Works perfectly on Python 3.13 + Windows.

Install:
  pip install deepface opencv-python tf-keras

First time setup:
  Say "register my face" to JARVIS — it opens your camera and saves your face.
  Then set FACE_LOGIN = True in config/settings.py
"""

import os
import cv2
import numpy as np


def _face_dir(settings) -> str:
    path = os.path.join(settings.LOG_DIR, "face_data")
    os.makedirs(path, exist_ok=True)
    return path


def _face_image_path(settings) -> str:
    return os.path.join(_face_dir(settings), "owner.jpg")


# ── Public API ────────────────────────────────────────────

def run(command: str, settings) -> dict:
    if any(k in command for k in ["register", "enroll", "train", "save my face"]):
        return _register(settings)
    return _verify_command(settings)


def verify_at_startup(settings) -> bool:
    """
    Called from jarvis.py before greeting.
    Returns True = access granted, False = denied.
    """
    face_path = _face_image_path(settings)
    if not os.path.exists(face_path):
        print("[Face] No face registered yet — skipping check.")
        return True

    try:
        from deepface import DeepFace
    except ImportError:
        print("[Face] DeepFace not installed — skipping face check.")
        return True

    print("\n🔐 Face verification — please look at the camera…")

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("[Face] No camera found — skipping face check.")
        return True

    verified = False
    attempts = 0

    while attempts < 40:           # Try for ~4 seconds
        ret, frame = cam.read()
        if not ret:
            attempts += 1
            continue

        # Show live preview
        cv2.imshow("JARVIS — Face Verification (hold still)", frame)
        cv2.waitKey(1)

        # Save temp frame and compare
        tmp = os.path.join(_face_dir(settings), "_tmp.jpg")
        cv2.imwrite(tmp, frame)

        try:
            result = DeepFace.verify(
                img1_path = tmp,
                img2_path = face_path,
                model_name     = "VGG-Face",
                enforce_detection = False,
            )
            if result.get("verified"):
                verified = True
                break
        except Exception:
            pass

        attempts += 1

    cam.release()
    cv2.destroyAllWindows()

    # Clean up temp file
    tmp = os.path.join(_face_dir(settings), "_tmp.jpg")
    if os.path.exists(tmp):
        os.remove(tmp)

    if verified:
        print("✅  Face recognised — Welcome back!")
    else:
        print("❌  Face not recognised. Access denied.")

    return verified


# ── Register ──────────────────────────────────────────────

def _register(settings) -> dict:
    import threading
    t = threading.Thread(target=_do_register, args=(settings,), daemon=True)
    t.start()
    return {
        "reply": (
            "Opening camera to register your face. "
            "Look directly at the camera and hold still. "
            "I'll save your face automatically!"
        )
    }


def _do_register(settings):
    """Opens camera, captures a clear face frame, and saves it."""
    try:
        from deepface import DeepFace
    except ImportError:
        print("\n[Face] DeepFace not installed.")
        print("Run: pip install deepface tf-keras")
        return

    face_path = _face_image_path(settings)

    print("\n📸  Registering face — look at the camera…")
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("[Face] No camera detected.")
        return

    saved = False
    for _ in range(80):            # Try for ~8 seconds
        ret, frame = cam.read()
        if not ret:
            continue

        cv2.imshow("JARVIS — Face Registration (press Q to quit)", frame)
        if cv2.waitKey(50) & 0xFF == ord('q'):
            break

        # Check a face is actually visible before saving
        tmp = os.path.join(_face_dir(settings), "_reg_tmp.jpg")
        cv2.imwrite(tmp, frame)

        try:
            faces = DeepFace.extract_faces(
                img_path = tmp,
                enforce_detection = True,
            )
            if faces:
                cv2.imwrite(face_path, frame)
                print(f"✅  Face registered and saved to {face_path}")
                print("    Now set  FACE_LOGIN = True  in config/settings.py")
                saved = True
                break
        except Exception:
            pass   # No face detected in this frame yet

    cam.release()
    cv2.destroyAllWindows()

    # Clean up
    tmp = os.path.join(_face_dir(settings), "_reg_tmp.jpg")
    if os.path.exists(tmp):
        os.remove(tmp)

    if not saved:
        print("❌  No face detected. Try again in better lighting.")


def _verify_command(settings) -> dict:
    ok = verify_at_startup(settings)
    if ok:
        return {"reply": "Face recognised! Identity verified."}
    return {"reply": "Face not recognised. Access denied."}
