from django.conf import settings
from twilio.rest import Client

twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

def send_whatsapp_message(to, message):
    twilio_client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body=message,
        to=to,
    )
