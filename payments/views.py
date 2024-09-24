from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from .coinpayments import CoinPaymentsAPI
from django.shortcuts import render
from django.http import JsonResponse
from .coinpayments import CoinPaymentsAPI
from decouple import config
from django.http import HttpResponseRedirect
import logging

logger = logging.getLogger(__name__)


# except Exception as e:
#     logger.error(f"Error processing payment: {e}")
#     return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)

def create_subscription(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        email = request.POST.get('email')
        coinpayments = CoinPaymentsAPI()
        payment_response = coinpayments.create_payment(amount, 'USD', email, 'subscription_plan')
        
        if payment_response.get('error') == 'ok':
            payment_url = payment_response['result']['checkout_url']
            return HttpResponseRedirect(payment_url)  # Redirect to CoinPayments payment page
        else:
            return JsonResponse({'status': 'error', 'message': payment_response.get('error')})

@csrf_exempt
def coinpayments_webhook(request):
    if request.method == 'POST':
        # Verify the HMAC signature from CoinPayments
        hmac_header = request.META.get('HTTP_HMAC')
        ipn_data = request.POST.dict()
        
        coinpayments = CoinPaymentsAPI(
            public_key="your_public_key",
            private_key="your_private_key",
            ipn_secret="your_ipn_secret"
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
