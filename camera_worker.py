import cv2
import requests
import argparse
import mediapipe as mp
import time

# ============================
# NGROK BACKEND URLS
# ============================

API_URL = "https://disinterestedly-unretaliatory-pearlene.ngrok-free.dev/event"
HEARTBEAT_URL = "https://disinterestedly-unretaliatory-pearlene.ngrok-free.dev/worker-heartbeat"

# ============================
# ARGUMENT PARSER
# ============================

parser = argparse.ArgumentParser()
parser.add_argument("--camera_id", required=True)
args = parser.parse_args()

camera_id = args.camera_id

# ============================
# MEDIAPIPE SETUP (0.10.x SAFE)
# ============================

mp_face = mp.solutions.face_detection
face_detector = mp_face.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.6
)

# ============================
# START CAMERA
# ============================

cap = cv2.VideoCapture(0)

print(f"[INFO] Camera Worker Started for {camera_id}")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detector.process(rgb_frame)

    if results.detections:
        print("[EVENT] Face Detected")

        try:
            requests.post(API_URL, json={
                "camera_id": camera_id,
                "event_type": "face_detected"
            })
        except Exception as e:
            print("Event send failed:", e)

    # Send heartbeat every 10 sec
    try:
        requests.post(HEARTBEAT_URL, json={
            "camera_id": camera_id
        })
    except:
        pass

    cv2.imshow("Camera Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(2)

cap.release()
cv2.destroyAllWindows()
