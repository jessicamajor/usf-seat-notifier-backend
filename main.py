from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from scraper import get_seats
from notifier import send_sms
from monitor import run_monitor
import json

app = FastAPI(title="USF Seat Notifier API")

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "USF Seat API running"}

# 1️⃣ Check seats instantly
@app.get("/check")
def check_seats(crn: str, term: str = "202601"):
    seats = get_seats(crn, term)
    return {"crn": crn, "term": term, "seats": seats}

# 2️⃣ Subscribe to automatic notifications
@app.post("/subscribe")
def subscribe(phone: str, crn: str, term: str = "202601"):
    sub = {"phone": phone, "crn": crn, "term": term, "last_seats": 0}

    with open("subscriptions.json", "r") as f:
        subs = json.load(f)

    subs.append(sub)

    with open("subscriptions.json", "w") as f:
        json.dump(subs, f)

    return {"status": "subscribed", "crn": crn, "phone": phone}

# 3️⃣ RUN MONITOR (Railway Cron calls this)
@app.get("/run-monitor")
def run_monitor_route():
    return run_monitor()
