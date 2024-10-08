import requests
import hashlib
import hmac
import time
from decouple import config
from django.http import JsonResponse
from django.utils.timezone import now
from datetime import timedelta

class CoinPaymentsAPI:
    def __init__(self):
        self.public_key = config('COINPAYMENTS_PUBLIC_KEY')
        self.private_key = config('COINPAYMENTS_PRIVATE_KEY')
        self.api_url = "https://www.coinpayments.net/api.php"

    def create_payment(self, amount, currency, buyer_email, subscription_plan):
        # Map fiat currency to cryptocurrency
        currency_mapping = {
            "USDC": "USDC",  # Map to USDC (ERC-20)
            "LTC": "LTC",    # Map to Litecoin (LTC)
        }

        # Use currency mapping or default to BTC
        currency2 = currency_mapping.get(currency, "BTC")  # Default to BTC if currency not found

        # Construct the payload for the CoinPayments API
        payload = {
            "cmd": "create_transaction",         # Command to create a transaction
            "amount": amount,                    # The amount in USD (or USDC equivalent)
            "currency1": "USD",                  # Currency1 is the fiat currency (USD)
            "currency2": currency2,              # Currency2 is the cryptocurrency (e.g., USDC, LTC)
            "buyer_email": buyer_email,          # The buyer's email
            "item_name": subscription_plan,      # Name of the subscription plan
            "ipn_url": "https://blog-a-878baae2c14f.herokuapp.com/api/payments/ipn-handler/",  # IPN handler URL
            "key": self.public_key,              # Your public API key
        }

        # Send the payload to the CoinPayments API and get the response
        payment_response = self._post(payload)

        # Process the API response
        if 'error' not in payment_response or payment_response['error'] == 'ok':
            # Successful response; return payment data for frontend
            return JsonResponse({
                'address': payment_response['result']['address'],        # Payment address
                'amount': payment_response['result']['amount'],          # Amount to send in the selected crypto
                'qr_code': payment_response['result']['qrcode_url'],     # QR code URL for easier payment
                'currency': currency2,                                   # Selected cryptocurrency
            }, status=200)
        else:
            # If there's an error in the API response
            return JsonResponse({'error': payment_response.get('error', 'Unknown error')}, status=400)

    def _post(self, data):
        # Add version, format, and nonce to payload
        data['version'] = 1
        data['format'] = 'json'
        data['nonce'] = str(int(time.time() * 1000))  # Unique nonce

        headers = {
            'hmac': hmac.new(
                self.private_key.encode(),
                requests.compat.urlencode(data).encode(),
                hashlib.sha512
            ).hexdigest()
        }

        try:
            # Send the request to CoinPayments API
            response = requests.post(self.api_url, data=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
            return {'error': str(e)}

    def validate_ipn(self, hmac_header, ipn_data):
        # Validate the IPN data using HMAC signature
        calculated_hmac = hmac.new(self.private_key.encode(), requests.compat.urlencode(ipn_data).encode(), hashlib.sha512).hexdigest()
        return hmac_header == calculated_hmac
