from twilio.rest import Client
import os

def send_sms(phone: str, message: str):
    sid = os.getenv("TWILIO_SID")
    auth = os.getenv("TWILIO_AUTH")
    number = os.getenv("TWILIO_NUMBER")

    if not sid or not auth or not number:
        print("Twilio not configured")
        return {"status": "twilio_not_configured"}

    client = Client(sid, auth)
    try:
        client.messages.create(
            body=message,
            from_=number,
            to=phone
        )
        return {"status": "sent"}
    except Exception as e:
        print("SMS error:", e)
        return {"status": "error", "details": str(e)}
