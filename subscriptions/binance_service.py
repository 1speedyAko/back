# subscriptions/binance_service.py
import requests
import hmac
import hashlib
import time
from django.conf import settings

class BinancePaymentService:
    def __init__(self):
        self.api_key = settings.BINANCE_API_KEY
        self.secret_key = settings.BINANCE_API_SECRET
        self.base_url = "https://bpay.binanceapi.com"

    def create_payment(self, order_id, amount, currency):
        url = f"{self.base_url}/binancepay/openapi/v2/order"
        payload = {
            "merchantTradeNo": order_id,
            "totalAmount": amount,
            "currency": currency,
            "productType": "Subscription",
            "productName": "Subscription Payment",
            "returnUrl": "https://predictoriouszone.vercel.app/thank-you"
        }
        headers = self._get_headers(payload)

        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        return response_data.get("data", {}).get("checkoutUrl", None)

    def _get_headers(self, payload):
        timestamp = str(int(time.time() * 1000))
        payload_str = str(payload)
        signature = hmac.new(
            self.secret_key.encode(),
            msg=(timestamp + payload_str).encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        return {
            "Content-Type": "application/json",
            "BinancePay-Timestamp": timestamp,
            "BinancePay-Signature": signature,
            "BinancePay-Certificate-SN": self.api_key
        }
