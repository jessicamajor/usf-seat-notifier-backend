from fastapi import FastAPI, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from scraper import get_seats
from notifier import send_sms

app = FastAPI(title="USF Seat Notifier API")

# Allow frontend to call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # allow your Base44 frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check route (required by Railway)
@app.get("/")
def root():
    return {"message": "USF Seat API running"}

# 1️⃣ Check seats RIGHT NOW
@app.get("/check")
def check_seats(
    crn: str = Query(...),
    term: str = Query("202601")
):
    seats = get_seats(crn, term)
    return {
        "crn": crn,
        "term": term,
        "seats": seats
    }

# 2️⃣ Send immediate SMS notification with current seats
@app.post("/notify")
def notify(
    phone: str,
    crn: str,
    term: str = "202601"
):
    seats = get_seats(crn, term)
