from ultralytics import YOLO
import cv2
import winsound
import time

# ---------------- LOAD MODEL ----------------
model = YOLO("best.pt")

# ---------------- STREAM URL ----------------
stream_url = "http://kamera.mikulov.cz:8888/mjpg/video.mjpg"

# ---------------- OPENCV SETTINGS ----------------
cv2.setLogLevel(0)  # suppress ffmpeg warnings

cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)

# Check stream
if not cap.isOpened():
    print("❌ ERROR: Unable to open video stream")
    exit()

print("✅ Stream connected")

alert_triggered = False
last_alert_time = 0
ALERT_COOLDOWN = 10  # seconds

# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = cap.read()

    if not ret:
        print("⚠️ Stream lost, reconnecting...")
        cap.release()
        time.sleep(3)
        cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
        continue

    # Resize for faster inference
    frame = cv2.resize(frame, (640, 480))

    # YOLO inference
    results = model.predict(
        source=frame,
        conf=0.5,
        verbose=False
    )

    for r in results:
        if r.boxes is None:
            continue

        for box in r.boxes:
            class_id = int(box.cls[0])
            class_name = r.names[class_id]
            confidence = float(box.conf[0])

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(
                frame,
                f"{class_name} {confidence:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2
            )

            # ---------------- ALERT LOGIC ----------------
            current_time = time.time()
            if (
                class_name.lower() == "severe"
                and confidence > 0.5
                and current_time - last_alert_time > ALERT_COOLDOWN
            ):
                print("🚨 ALERT: Severe accident detected!")
                winsound.Beep(1200, 1000)
                last_alert_time = current_time

    # Display output
    cv2.imshow("AI Accident Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ---------------- CLEANUP ----------------
cap.release()
cv2.destroyAllWindows()
