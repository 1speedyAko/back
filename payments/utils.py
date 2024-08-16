import requests
import uuid
import hmac
import hashlib
from django.conf import settings
from .models import Payment

CRYPTOMUS_API_URL = "https://api.cryptomus.com/v1/recurrence/create"

def create_payment(user, product, amount, currency):
    order_id = str(uuid.uuid4())
    period = (
        "monthly" if product.category == 'silver' else
        "bi-monthly" if product.category == 'gold' else
        "quarterly"
    )

    payload = {
        "amount": str(amount),
        "currency": currency,
        "name": f"{product.name} - Recurring payment",
        "period": period,
        "url_callback": f"{settings.SITE_URL}/callback"  # Update this with your callback URl
    }

    headers = {
        'merchant': settings.CRYPTOMUS_MERCHANT_ID,
        'sign': _generate_signature(payload),
        'Content-Type': 'application/json'
    }

    response = requests.post(CRYPTOMUS_API_URL, json=payload, headers=headers)
    response_data = response.json()

    if response.status_code == 200 and response_data.get('state') == 0:
        result = response_data['result']
        payment = Payment.objects.create(
            order_id=order_id,
            user=user,
            product=product,
            amount=amount,
            currency=currency,
            status='pending',
            transaction_id=result['uuid'],
            payment_url=result['url']  # Store the payment URL if needed
        )
        return {
            'status': 'confirmed',
            'payment': payment,
            'payment_url': result['url']  # Return the payment URL for redirecting the user
        }
    else:
        return {'status': 'failed', 'message': response_data.get('error', 'Unknown error')}

def _generate_signature(payload):
    secret = settings.CRYPTOMUS_API_KEY
    message = f"{payload['amount']}{payload['currency']}{payload['period']}"
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
    return signature

def validate_webhook_signature(payload, signature):
    secret = settings.SECRET_KEY
    expected_signature = hmac.new(
        key=secret.encode(),
        msg=str(payload).encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected_signature, signature)
