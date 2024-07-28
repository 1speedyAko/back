import requests
from django.conf import settings

def initiate_payment(user, product_id, amount, currency):
    # Implement your Cryptomus payment initiation logic here
    # For example:
    response = requests.post('https://cryptomus.com/api/initiate', data={
        'user': user.id,
        'product_id': product_id,
        'amount': amount,
        'currency': currency,
    })

    if response.status_code == 200:
        return response.json()
    else:
        return {'status': 'failed', 'message': 'Unable to initiate payment'}

def verify_payment(payment):
    # Implement your Cryptomus payment verification logic here
    # For example:
    response = requests.post('https://cryptomus.com/api/verify', data={
        'transaction_id': payment.transaction_id,
    })

    if response.status_code == 200:
        return response.json()
    else:
        return {'status': 'failed', 'message': 'Unable to verify payment'}
