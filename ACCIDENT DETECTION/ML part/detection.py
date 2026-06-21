import os
import random
import winsound
from ultralytics import YOLO

# ---------------------------------
# LOAD MODEL
# ---------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "best.pt")

if os.path.exists(MODEL_PATH):
    model = YOLO(MODEL_PATH)
    print("✅ Model loaded:", MODEL_PATH)
else:
    model = None
    print("⚠️ best.pt not found → DEMO MODE")


# ---------------------------------
# DETECTION CLASS
# ---------------------------------
class Detection:

    @staticmethod
    def prediction(path):
        """
        Detect from IMAGE only (NO CAMERA)
        """

        # -------- DEMO MODE --------
        if model is None or not os.path.exists(path):
            print("⚠️ DEMO MODE running")

            event_id = random.choice([0, 1, 2, 3])
            confidence = random.uniform(0.7, 1.0)
            return [event_id, confidence]

        # -------- REAL YOLO DETECTION --------
        results = model.predict(source=path, conf=0.5, verbose=False)

        for r in results:
            if r.boxes and len(r.boxes) > 0:
                box = r.boxes[0]

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                winsound.Beep(1200, 200)

                return [class_id, confidence]

        return [-1, 0.0]
