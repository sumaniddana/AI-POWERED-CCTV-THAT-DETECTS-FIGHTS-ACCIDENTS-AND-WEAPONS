# ==============================
# BUZZ_LED.py  (SIMULATION MODE)
# Mobile Alert Only (Pushbullet)
# No Camera Required
# ==============================

import time
import random
import requests
import os

# ==================================================
# 🔔 PUT YOUR PUSHBULLET TOKEN HERE
# ==================================================
PUSHBULLET_TOKEN = "o.hwK9ZrMM0W8v6TH3D16rVVfmGBaMqHGV"
# get from -> https://www.pushbullet.com/#settings/account
# ==================================================


# ==================================================
# PUSHBULLET FUNCTION
# ==================================================
def send_mobile_alert(title, message):
    try:
        url = "https://api.pushbullet.com/v2/pushes"

        headers = {
            "Access-Token": PUSHBULLET_TOKEN,
            "Content-Type": "application/json"
        }

        data = {
            "type": "note",
            "title": title,
            "body": message
        }

        requests.post(url, json=data, headers=headers)

        print("📱 Alert sent to mobile")

    except Exception as e:
        print("Pushbullet Error:", e)


# ==================================================
# LED SIMULATION (Windows Safe)
# ==================================================
def leds_off():
    print("LEDs OFF")


def green_led():
    print("🟢 GREEN LED (SAFE)")


def red_led():
    print("🔴 RED LED (ALERT)")


# ==================================================
# EVENT ALERT HANDLER
# ==================================================
def event_alert(event_name):
    red_led()

    send_mobile_alert(
        "🚨 CCTV ALERT",
        f"{event_name} detected!"
    )

    time.sleep(2)
    leds_off()


# ==================================================
# OPTIONAL MODEL LOAD (SAFE)
# ==================================================
MODEL_PATH = r"C:\Users\suman\OneDrive\Desktop\AI-POWERED CCTV THAT DETECTS FIGHTS, ACCIDENTS AND WEAPONS\ACCIDENT DETECTION\ML part\best.pt"

if os.path.exists(MODEL_PATH):
    print(f"✅ Model loaded: {MODEL_PATH}")
else:
    print("⚠ Model not found (not required for simulation)")


# ==================================================
# MAIN PROGRAM
# ==================================================
print("\nSystem started")
print("Running on Windows (SIMULATION MODE)")
print("Mobile alerts enabled\n")

leds_off()

try:
    while True:
        green_led()

        # wait before next check
        time.sleep(5)

        # 20% chance to trigger event
        if random.random() < 0.2:

            event = random.choice([
                "Accident",
                "Violence",
                "Weapon Detected",
                "Fight"
            ])

            print("🚨 EVENT:", event)
            event_alert(event)

        else:
            print("No event detected")

except KeyboardInterrupt:
    print("\nStopped safely")
    leds_off()
