# cryptomus.py
import requests
import uuid
from django.conf import settings
from .models import Payment

CRPYTOMUS_API_URL = "https://api.cryptomus.com/v1/recurrence/create"

def create_payment(user, product, amount, currency):
    order_id = str(uuid.uuid4())
    payload = {
        "amount": str(amount),
        "currency": currency,
        "name": product.name,
        "period": "monthly" if product.category == 'silver' else "bi-monthly" if product.category == 'gold' else "quarterly"
    }

    headers = {
        'merchant': settings.CRYPTOMUS_MERCHANT_ID,
        'sign': settings.CRYPTOMUS_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.post(CRPYTOMUS_API_URL, json=payload, headers=headers)
    response_data = response.json()

    if response.status_code == 200 and response_data['state'] == 0:
        payment = Payment.objects.create(
            order_id=order_id,
            user=user,
            product=product,
            amount=amount,
            currency=currency,
            status='confirmed',
            transaction_id=response_data['result']['uuid']
        )
        return {'status': 'confirmed', 'payment': payment}
    else:
        return {'status': 'failed', 'message': response_data.get('error', 'Unknown error')}


