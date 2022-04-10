from twilio.rest import Client
from django.conf import settings

twilio_api = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def fetch_sms():
    return twilio_api.messages.stream()