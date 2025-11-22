import json

with open("config.json") as f:
    config = json.load(f)

USE_TWILIO = config.get("use_twilio", False)

if USE_TWILIO:
    from twilio.rest import Client
    TWILIO_SID = config["twilio_sid"]
    TWILIO_AUTH = config["twilio_auth"]
    TWILIO_NUMBER = config["twilio_number"]
    client = Client(TWILIO_SID, TWILIO_AUTH)
else:
    TWILIO_NUMBER = None  # not used

def send_sms(phone: str, crn: str, seats: int):
    message = f"Seats AVAILABLE for CRN {crn}! {seats} seats remaining."
    if USE_TWILIO:
        client.messages.create(body=message, from_=TWILIO_NUMBER, to=phone)
    else:
        # For testing without Twilio charges
        print(f"[FAKE SMS] to {phone}: {message}")
