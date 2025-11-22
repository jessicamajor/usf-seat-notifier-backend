from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select
from db import init_db, get_session
from models import Subscription
from background import start_background_monitor

app = FastAPI(title="USF Seat Notifier")

# Allow calls from anywhere (useful if you later add a frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB and start background seat monitor when app starts
init_db()
start_background_monitor()

@app.get("/")
def root():
    return {"message": "USF Seat Notifier API running"}

@app.get("/subscriptions")
def list_subscriptions():
    with get_session() as session:
        subs = session.exec(select(Subscription)).all()
        return subs

@app.post("/subscribe")
def subscribe(phone: str, crn: str):
    with get_session() as session:
        sub = Subscription(phone=phone, crn=crn)
        session.add(sub)
        session.commit()
        session.refresh(sub)
        return sub

@app.delete("/unsubscribe/{sub_id}")
def unsubscribe(sub_id: int):
    with get_session() as session:
        sub = session.get(Subscription, sub_id)
        if not sub:
            return {"error": "Subscription not found"}

        session.delete(sub)
        session.commit()
        return {"status": "unsubscribed"}
