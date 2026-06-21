from ultralytics import YOLO
import winsound

model = YOLO("best.pt")

video_path = "inputs/videos/video1.mp4"

results = model.predict(source=video_path, save=True, show=True)

for r in results:
    for box in r.boxes:
        class_id = r.names[int(box.cls[0])]
        confidence = float(box.conf[0])

        print("Detected:", class_id)
        print("Confidence:", confidence)

        if class_id == "severe" and confidence > 0.5:
            print("🚨 ALERT: Severe accident detected!")
            winsound.Beep(1200, 800)

        print("----")
