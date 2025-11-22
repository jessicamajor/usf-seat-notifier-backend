from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from scraper import get_seats
from notifier import send_sms
from monitor import add_subscription, run_monitor

app = FastAPI(title="USF Seat Notifier API")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/")
def root():
    return {"message": "USF Seat API running"}

# 1) Check seats instantly
@app.get("/check")
def check_seats(
    crn: str,
    term: str = "202601"
):
    seats = get_seats(crn, term)
    return {"crn": crn, "term": term, "seats": seats}

# 2) Subscribe phone + CRN
@app.post("/subscribe")
def subscribe(
    phone: str,
    crn: str,
    term: str = "202601"
):
    sub = add_subscription(phone, crn, term)
    return {"status": "subscribed", "subscription": sub}

# 3) Monitor trigger (Railway cron calls this)
@app.get("/run-monitor")
def run_monitor_route():
    return run_monitor()
