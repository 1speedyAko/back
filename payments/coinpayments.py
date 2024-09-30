import requests
import hashlib
import hmac
import time
from decouple import config

class CoinPaymentsAPI:
    def __init__(self):
        self.public_key = config('COINPAYMENTS_PUBLIC_KEY')
        self.private_key = config('COINPAYMENTS_PRIVATE_KEY')
        self.api_url = "https://www.coinpayments.net/api.php"

    def create_payment(self, amount, currency, buyer_email, subscription_plan):
    # Define a mapping between fiat currencies and cryptocurrency counterparts
        currency_mapping = {
            "USD": "USDC",  # Map USD to USDC for CoinPayments
            "BTC": "BTC",
            # Add other mappings as needed
        }

        # Map the provided currency to the correct cryptocurrency
        currency2 = currency_mapping.get(currency, "BTC")  # Default to BTC if currency not in mapping

        # Construct the payload
        payload = {
            "cmd": "create_transaction",
            "amount": amount,
            "currency1": "USD",  # Currency1 is USD (fiat)
            "currency2": currency2,  # Mapped cryptocurrency (e.g., USDC, BTC, ETH)
            "buyer_email": buyer_email,
            "item_name": subscription_plan,
            "ipn_url": "https://blog-a-878baae2c14f.herokuapp.com/api/payments/ipn-handler/",  # IPN handler URL
            "key": self.public_key,
        }

        # Send the payload to the CoinPayments API
        return self._post(payload)


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
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
            return {'error': str(e)}

    def validate_ipn(self, hmac_header, ipn_data):
        calculated_hmac = hmac.new(self.private_key.encode(), requests.compat.urlencode(ipn_data).encode(), hashlib.sha512).hexdigest()
        return hmac_header == calculated_hmac
