from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .coinpayments import CoinPaymentsAPI
from django.shortcuts import render
from django.http import JsonResponse
from .coinpayments import CoinPaymentsAPI
from decouple import config
def create_subscription(request):
    if request.method == 'POST':
        # Get subscription details from request data
        amount = request.POST.get('amount')
        email = request.POST.get('email')
        
        # Create a payment transaction
        coinpayments = CoinPaymentsAPI(
            public_key=config('COINPAYMENTS_PUBLIC_KEY'),
            private_key=config('COINPAYMENTS_PRIVATE_KEY'),
            ipn_secret=config('COINPAYMENTS_IPN_SECRET')
        )
        payment_response = coinpayments.create_payment(amount, 'USD', email, 'subscription_plan')
        
        # Handle payment response
        if payment_response.get('error') == 'ok':
            return JsonResponse({
                'status': 'success',
                'payment_url': payment_response['result']['checkout_url']
            })
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
