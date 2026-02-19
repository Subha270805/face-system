import cv2
import mediapipe as mp
import requests
from datetime import datetime

mp_face = mp.solutions.face_detection.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.5
)

cap = cv2.VideoCapture(0)
API_URL = "http://127.0.0.1:8000/event"

print("Starting camera worker... Press ESC to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera not accessible")
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = mp_face.process(rgb)

    if result.detections:
        print("Face detected!")
        payload = {
            "person": "unknown",
            "camera": "mac-webcam",
            "time": str(datetime.now())
        }
        try:
            r = requests.post(API_URL, json=payload, timeout=2)
            print("API:", r.status_code, r.text)
        except Exception as e:
            print("API call failed:", e)

    cv2.imshow("Face Worker", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

