import requests
import hmac
import hashlib

class CryptomusAPI:
    BASE_URL = 'https://api.cryptomus.com/v1'
    
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def create_invoice(self, amount, currency, order_id, callback_url):
        endpoint = f"{self.BASE_URL}/invoice"
        headers = {
            'API-KEY': self.api_key,
            'SECRET-KEY': self.secret_key,
        }
        payload = {
            'amount': amount,
            'currency': currency,
            'order_id': order_id,
            'callback_url': callback_url,
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        return response.json()

    def check_payment_status(self, order_id):
        endpoint = f"{self.BASE_URL}/invoice/status"
        headers = {
            'API-KEY': self.api_key,
            'SECRET-KEY': self.secret_key,
        }
        payload = {
            'order_id': order_id,
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        return response.json()

    def verify_signature(request):
        received_signature = request.headers.get('X-Signature')
        secret_key = settings.CRYPTO_SECRET_KEY

        body = request.body
        computed_signature = hmac.new(secret_key.encode(), body, hashlib.sha256).hexdigest()

        return hmac.compare_digest(received_signature, computed_signature)

# In settings.py or environment variables
CRYPTO_API_KEY = 'your_api_key'
CRYPTO_SECRET_KEY = 'your_secret_key'
