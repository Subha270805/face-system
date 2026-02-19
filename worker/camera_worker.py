import cv2
import time
import requests
import mediapipe as mp

API_URL = "http://127.0.0.1:8000/event"

mp_face = mp.solutions.face_detection.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.5
)

cap = cv2.VideoCapture(0)

print("🟢 Camera worker started. Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Camera read failed")
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = mp_face.process(rgb)

    if result.detections:
        print("🙂 Face detected!")

        payload = {
            "person": "unknown",
            "camera": "mac-webcam"
        }

        try:
            r = requests.post(API_URL, json=payload, timeout=10)
            print("API:", r.status_code, r.json())
        except Exception as e:
            print("API error (ignored):", e)

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(2)

cap.release()
cv2.destroyAllWindows()

