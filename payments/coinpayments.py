import requests
import hashlib
import hmac
import time
from decouple import config

class CoinPaymentsAPI:
    def __init__(self):
        self.public_key = config('COINPAYMENTS_PUBLIC_KEY')
        self.private_key = config('COINPAYMENTS_PRIVATE_KEY')
        self.ipn_secret = config('COINPAYMENTS_IPN_SECRET')
        self.api_url = "https://www.coinpayments.net/api.php"

    def create_payment(self, amount, currency, buyer_email, custom):
        data = {
            'cmd': 'create_transaction',
            'amount': amount,
            'currency1': currency,  
            'currency2': 'BTC',     
            'buyer_email': buyer_email,
            'custom': custom,  
            'key': self.public_key
        }
        return self._post(data)

    def _post(self, data):
        data['version'] = 1
        data['format'] = 'json'
        data['nonce'] = str(int(time.time() * 1000))
    
        headers = {
            'hmac': hmac.new(
                self.private_key.encode(),
                requests.compat.urlencode(data).encode(),
                hashlib.sha512
            ).hexdigest()
        }
    
        try:
            response = requests.post(self.api_url, data=data, headers=headers)
            response.raise_for_status()  # Check if request was successful
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
            return {'error': str(e)}


    def validate_ipn(self, hmac_header, ipn_data):
        # Ensure that IPN message was not tampered with
        calculated_hmac = hmac.new(self.private_key.encode(), requests.compat.urlencode(ipn_data).encode(), hashlib.sha512).hexdigest()

        return hmac_header == calculated_hmac
