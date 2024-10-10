from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json
import requests
import hmac
import hashlib
import time
from .models import Payment

class BinancePaymentView(APIView):
    def post(self, request, format=None):
        user = request.user
        amount = request.data['amount']
        currency = request.data.get('currency', 'USD')
        order_id = f"{user.id}-{int(time.time())}"

        # Call Binance API to create a payment request
        headers = {
            'X-MBX-APIKEY': 'your_api_key'
        }

        payload = {
            'amount': amount,
            'currency': currency,
            'merchant_order_id': order_id,
        }

        # Sign payload with HMAC SHA256
        secret = 'your_api_secret'
        query_string = '&'.join([f"{k}={v}" for k, v in payload.items()])
        signature = hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
        payload['signature'] = signature

        response = requests.post(
            'https://api.binance.com/api/v3/order',
            headers=headers,
            data=payload
        )

        if response.status_code == 200:
            # Save payment record
            payment = Payment.objects.create(
                user=user,
                amount=amount,
                currency=currency,
                status='pending',
                order_id=order_id,
            )
            return Response({"payment_url": response.json()['url']}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": response.json()}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def binance_ipn_handler(request):
    data = json.loads(request.body)
    transaction_id = data['transaction_id']
    status = data['status']
    order_id = data['merchant_order_id']

    # Update payment status in the database
    try:
        payment = Payment.objects.get(order_id=order_id)
        payment.status = 'confirmed' if status == 'SUCCESS' else 'failed'
        payment.transaction_id = transaction_id
        payment.save()
        return JsonResponse({'status': 'success'}, status=200)
    except Payment.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
