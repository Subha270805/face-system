import cv2
import time
import requests
import mediapipe as mp
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--camera_id", default="cam1")
parser.add_argument("--source", default=0)
args = parser.parse_args()

CAMERA_ID = args.camera_id
SOURCE = int(args.source)

# 🔥 Debug: show which worker booted
print(f"🔥 Worker booted with CAMERA_ID = {CAMERA_ID}")

# ✅ Dev B backend exposed via ngrok
API_URL = "https://disinterestedly-unretaliatory-pearlene.ngrok-free.dev/event"

mp_face = mp.solutions.face_detection.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.5
)

cap = cv2.VideoCapture(SOURCE)
print(f"🟢 Camera worker started for {CAMERA_ID}. Press Q to quit.")

# 🚀 Demo heartbeat: send one startup event per worker (so cam2–cam5 appear even if webcam is busy)
try:
    requests.post(API_URL, json={"person": "Startup", "camera": CAMERA_ID}, timeout=5)
    print(f"🚀 Startup event sent for {CAMERA_ID}")
except Exception as e:
    print("❌ Startup event failed:", e)

last_sent = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to read from camera")
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_face.process(rgb)

    # Send event every 5 seconds when a face is detected
    if results.detections and time.time() - last_sent > 5:
        payload = {
            "person": "Unknown",
            "camera": CAMERA_ID
        }
        try:
            r = requests.post(API_URL, json=payload, timeout=5)
            print(f"📡 Sent event to backend: {r.status_code}")
            last_sent = time.time()
        except Exception as e:
            print("❌ Failed to send event:", e)

    cv2.imshow(f"Camera - {CAMERA_ID}", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
