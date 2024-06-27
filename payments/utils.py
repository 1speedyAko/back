# payments/utils.py
import requests
from django.conf import settings

def create_charge(amount, currency, buyer_email, item_name):
    url = 'https://www.coinpayments.net/api.php'
    payload = {
        'key': settings.COINPAYMENTS_API_KEY,
        'cmd': 'create_transaction',
        'amount': amount,
        'currency1': 'USD',
        'currency2': currency,
        'buyer_email': buyer_email,
        'item_name': item_name,
        'format': 'json'
    }
    
    headers = {
        'Content-Type': 'application/json',
        'HMAC': settings.COINPAYMENTS_API_SECRET
    }

    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    
    if response_data['error'] == 'ok':
        return response_data['result']
    else:
        raise Exception(response_data['error'])
