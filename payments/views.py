from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from .coinpayments import CoinPaymentsAPI
from django.http import JsonResponse
from .coinpayments import CoinPaymentsAPI
from decouple import config
from django.views.decorators.csrf import csrf_exempt
import json

from django.http import HttpResponseRedirect
import logging

logger = logging.getLogger(__name__)


# except Exception as e:
#     logger.error(f"Error processing payment: {e}")
#     return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)

@csrf_exempt
def create_subscription(request):
    if request.method == 'POST':
        # Load data from JSON body
        try:
            data = json.loads(request.body)
            amount = data.get('amount')
            email = data.get('email')
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        coinpayments = CoinPaymentsAPI()
        payment_response = coinpayments.create_payment(amount, 'USD', email, 'subscription_plan')
        
        if payment_response.get('error') == 'ok':
            payment_url = payment_response['result']['checkout_url']
            return JsonResponse({'payment_url': payment_url}, status=200)  # Return the payment URL
        else:
            return JsonResponse({'status': 'error', 'message': payment_response.get('error')})
@csrf_exempt
def coinpayments_webhook(request):
    if request.method == 'POST':
        # Verify the HMAC signature from CoinPayments
        hmac_header = request.META.get('HTTP_HMAC')
        ipn_data = request.body.decode()
        
        coinpayments = CoinPaymentsAPI(
            public_key=config('COINPAYMENTS_PUBLIC_KEY'),
            private_key=config('COINPAYMENTS_PRIVATE_KEY'),
            ipn_secret=config('COINPAYMENTS_IPN_SECRET')
        )

        # Validate IPN response (add your custom logic)
        if coinpayments.validate_ipn(hmac_header, ipn_data):
            # Handle successful payment or subscription event
            txn_id = ipn_data.get('txn_id')
            status = ipn_data.get('status')
            
            # Update payment or subscription status in your database
            return HttpResponse('IPN received', status=200)
        else:
            return HttpResponse('Invalid IPN', status=400)
