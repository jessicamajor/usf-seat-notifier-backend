from twilio.rest import Client
import os

def send_sms(phone: str, message: str):
    sid = os.getenv("TWILIO_SID")
    auth = os.getenv("TWILIO_AUTH")
    number = os.getenv("TWILIO_NUMBER")

    if not sid or not auth or not number:
        return {"status": "twilio_not_configured"}

    try:
        client = Client(sid, auth)
        client.messages.create(body=message, from_=number, to=phone)
        return {"status": "sent"}
    except Exception as e:
        return {"status": "error", "details": str(e)}
