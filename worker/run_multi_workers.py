import json
import subprocess
import time

with open("config/cameras.json") as f:
    cams = json.load(f)["cameras"]

procs = []

for cam in cams:
    print(f"Starting worker for {cam['id']}")
    p = subprocess.Popen([
        "python", "camera_worker.py",
        "--camera_id", cam["id"],
        "--source", str(cam["source"])
    ])
    procs.append(p)
    time.sleep(1)

print("All workers started. Monitoring workers...")

while True:
    for i, p in enumerate(procs):
        if p.poll() is not None:
            cam = cams[i]
            print("Worker crashed. Restarting", cam["id"])
            procs[i] = subprocess.Popen([
                "python", "camera_worker.py",
                "--camera_id", cam["id"],
                "--source", str(cam["source"])
            ])
    time.sleep(5)
