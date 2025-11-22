import time
import threading
import json
from sqlmodel import select
from db import get_session
from models import Subscription
from scraper import get_seats
from notifier import send_sms

with open("config.json") as f:
    config = json.load(f)

TERM = config.get("term", "202601")
POLL_SECONDS = config.get("poll_seconds", 60)

def monitor_loop():
    while True:
        with get_session() as session:
            subs = session.exec(select(Subscription)).all()
            for sub in subs:
                seats = get_seats(sub.crn, TERM)
                if seats > 0 and sub.last_seats == 0:
                    send_sms(sub.phone, sub.crn, seats)
                sub.last_seats = seats
                session.add(sub)
            session.commit()

        time.sleep(POLL_SECONDS)

def start_background_monitor():
    thread = threading.Thread(target=monitor_loop, daemon=True)
    thread.start()