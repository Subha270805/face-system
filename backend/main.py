from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "backend ok"}

@app.post("/event")
def create_event(payload: dict):
    print("EVENT RECEIVED:", payload)
    return {"received": True, "saved": True}

@app.get("/events")
def get_events():
    return {"events": []}


