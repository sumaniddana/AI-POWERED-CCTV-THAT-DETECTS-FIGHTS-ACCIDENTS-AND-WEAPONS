import cv2
import time
import random
import logging
import os
import requests
import winsound

from pathlib import Path
from datetime import datetime
from collections import Counter

import matplotlib.pyplot as plt
from dotenv import load_dotenv



# ================= SETTINGS =================

CAMERA_INDEX = 0

RUN_TIME = 5

SLOW_MOTION = 0.15

CONFIDENCE_THRESHOLD = 0.7



# ================= LOGGING =================

logging.basicConfig(
    filename="cctv_alert_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)



# ================= ENV =================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

TOKEN = os.getenv("PUSHBULLET_API_KEY")



# ================= LAPTOP ALERT =================

def laptop_alarm():

    for i in range(5):

        winsound.Beep(
            2500,
            700
        )

        time.sleep(0.2)



# ================= MOBILE ALERT =================

def send_mobile_alert(event, confidence):


    if not TOKEN:

        print("Pushbullet skipped")

        return


    try:

        url = "https://api.pushbullet.com/v2/pushes"


        headers = {

            "Access-Token": TOKEN,

            "Content-Type": "application/json"

        }



        message = f"""

🚨 CCTV WARNING 🚨


Detection:
{event}


Confidence:
{round(confidence*100,2)}%


Time:
{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}


CHECK CAMERA IMMEDIATELY

"""


        data = {

            "type":"note",

            "title":"🚨 Emergency Alert",

            "body":message,

            "priority":2,

            "sound":"alarm"

        }



        r=requests.post(
            url,
            json=data,
            headers=headers,
            timeout=3
        )


        if r.status_code==200:

            print(
                "Mobile Alert Sent"
            )


        else:

            print(
                "Internet unavailable"
            )


    except:

        print(
            "No internet - Laptop alert only"
        )





# ================= MODEL =================

try:

    from detection_module import Detection as DetectionModel

    print("ML Model Loaded")


except:


    print("Demo Mode Started")

    DetectionModel=None





# ================= EVENTS =================


event_map={

    0:"ACCIDENT",

    1:"SEVERE ACCIDENT",

    2:"VIOLENCE",

    3:"WEAPON"

}



counter=Counter()



# ================= CAMERA =================


cap=cv2.VideoCapture(
    CAMERA_INDEX
)


if not cap.isOpened():

    print("Camera not found")

    exit()



print("AI CCTV Started")

print("Press Q to stop")



start=time.time()

sent=set()



# ================= LIVE CCTV =================


while True:



    ret,frame=cap.read()


    if not ret:

        break



    if time.time()-start >= RUN_TIME:

        break



    time.sleep(
        SLOW_MOTION
    )



    if DetectionModel:


        event_id,confidence = DetectionModel.prediction(frame)



    else:


        event_id=random.randint(0,3)

        confidence=random.uniform(
            0.5,
            1.0
        )



    event=event_map[event_id]



    timestamp=datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )





    if confidence >= CONFIDENCE_THRESHOLD:


        counter[event]+=1


        print(
            "\n================"
        )

        print(
            "DETECTION:",
            event
        )

        print(
            "CONFIDENCE:",
            round(confidence,2)
        )

        print(
            "================"
        )



        logging.info(
            f"{event} detected {confidence}"
        )



        if event not in sent:


            # offline laptop sound

            laptop_alarm()



            # mobile if internet exists

            send_mobile_alert(
                event,
                confidence
            )


            sent.add(event)




    if confidence < 0.7:

        text="NORMAL"

        color=(0,255,0)


    elif event=="ACCIDENT":

        text="ACCIDENT DETECTED"

        color=(0,0,255)


    elif event=="SEVERE ACCIDENT":

        text="SEVERE ACCIDENT"

        color=(0,0,255)


    elif event=="VIOLENCE":

        text="VIOLENCE DETECTED"

        color=(255,0,0)


    else:

        text="WEAPON DETECTED"

        color=(0,255,255)




    cv2.putText(
        frame,
        text,
        (30,60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        3
    )



    cv2.putText(
        frame,
        "Time: "+timestamp,
        (30,110),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,255),
        2
    )


    cv2.putText(
        frame,
        "Confidence: "+str(round(confidence,2)),
        (30,150),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,255),
        2
    )



    cv2.imshow(
        "AI CCTV Detection",
        frame
    )



    if cv2.waitKey(1)&0xff==ord('q'):

        break





cap.release()

cv2.destroyAllWindows()





# ================= GRAPH =================


print(
    "Creating Graph"
)



plt.figure(
    figsize=(7,5)
)



if counter:


    plt.bar(
        counter.keys(),
        counter.values()
    )


else:


    plt.bar(
        ["NO EVENT"],
        [0]
    )



plt.title(
    "CCTV Detection Report"
)



plt.xlabel(
    "Detection Type"
)



plt.ylabel(
    "Count"
)



plt.xticks(
    rotation=30
)



plt.tight_layout()



plt.show(
    block=False
)



time.sleep(2)

plt.close()



print(
    "Project Completed"
)