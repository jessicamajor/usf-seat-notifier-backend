import json
import os
from scraper import get_seats
from notifier import send_sms

# Railway requires ALL writable files to be in /tmp
SUB_FILE = "/tmp/subscriptions.json"

def load_subs():
    # Ensure file exists
    if not os.path.exists(SUB_FILE):
        with open(SUB_FILE, "w") as f:
            f.write("[]")

    try:
        with open(SUB_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_subs(subs):
    with open(SUB_FILE, "w") as f:
        json.dump(subs, f)

def add_subscription(phone, crn, term):
    subs = load_subs()
    sub = {"phone": phone, "crn": crn, "term": term, "last_seats": 0}
    subs.append(sub)
    save_subs(subs)
    return sub

def run_monitor():
    subs = load_subs()
    changed = False

    for sub in subs:
        crn = sub["crn"]
        phone = sub["phone"]
        term = sub["term"]
        last = sub.get("last_seats", 0)

        seats = get_seats(crn, term)

        if seats is None:
            continue

        # notify when seats go from 0 -> >0
        if last == 0 and seats > 0:
            send_sms(phone, f"Seat OPEN for CRN {crn}! {seats} seats remaining.")

        sub["last_seats"] = seats
        changed = True

    if changed:
        save_subs(subs)

    return {"status": "checked", "subscriptions": len(subs)}
