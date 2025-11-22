import json
from scraper import get_seats
from notifier import send_sms

SUB_FILE = "subscriptions.json"

def load_subs():
    try:
        with open(SUB_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_subs(subs):
    with open(SUB_FILE, "w") as f:
        json.dump(subs, f)

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
            continue  # skip failures

        # Only notify when seats go from 0 → >0
        if last == 0 and seats > 0:
            send_sms(phone, f"Seat OPEN for CRN {crn}! {seats} seats remaining.")

        sub["last_seats"] = seats
        changed = True

    if changed:
        save_subs(subs)

    return {"status": "checked", "subscriptions": len(subs)}
