import hashlib
import hmac
import json
import requests
from django.conf import settings

CRYPTOMUS_API_URL = "https://api.cryptomus.com/v1/recurrence/create"
CRYPTOMUS_API_KEY = settings.CRYPTOMUS_API_KEY
CRYPTOMUS_SECRET_KEY = settings.COINPAYMENTS_API_SECRET

def create_signature(payload):
    return hmac.new(
        CRYPTOMUS_SECRET_KEY.encode(), 
        json.dumps(payload).encode(), 
        hashlib.sha256
    ).hexdigest()

def create_payment(amount, currency, period):
    endpoint = f"{CRYPTOMUS_API_URL}recurrence/create"
    headers = {
        "merchant": CRYPTOMUS_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "amount": amount,
        "currency": currency,
        "name": "Recurring payment",
        "period": period
    }
    headers["sign"] = create_signature(payload)
    response = requests.post(endpoint, headers=headers, json=payload)
    return response.json()

def validate_webhook_signature(payload, signature):
    return create_signature(payload) == signature
