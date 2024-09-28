from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .coinpayments import CoinPaymentsAPI
import json
import logging
from rest_framework.views import APIView
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)

@csrf_exempt
def create_subscription(request):
    if request.method == 'POST':
        # Load data from the JSON body
        try:
            data = json.loads(request.body)
            amount = data.get('amount')
            email = data.get('email')
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        # Create the payment transaction using CoinPaymentsAPI
        coinpayments = CoinPaymentsAPI()
        payment_response = coinpayments.create_payment(amount, 'USD', email, 'subscription_plan')
        
        # Handle the response from CoinPayments
        if payment_response.get('error') == 'ok':
            payment_url = payment_response['result']['checkout_url']
            return JsonResponse({'payment_url': payment_url}, status=200)  # Return the payment URL
        else:
            logger.error(f"Error processing payment: {payment_response.get('error')}")
            return JsonResponse({'status': 'error', 'message': payment_response.get('error')})

class CoinPaymentsIPNView(APIView):
    permission_classes = []  # No permissions as this will be a public endpoint

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        # Extract IPN data from the POST request
        ipn_data = request.POST

        # Get the HMAC signature sent by CoinPayments
        hmac_header = request.headers.get('HMAC')

        # Validate the IPN
        coinpayments = CoinPaymentsAPI()
        if not coinpayments.validate_ipn(hmac_header, ipn_data):
            return JsonResponse({'status': 'error', 'message': 'Invalid IPN'}, status=400)

        # Process the payment based on status
        status = ipn_data.get('status')  # Payment status
        txn_id = ipn_data.get('txn_id')  # Transaction ID

        if status == '100':  # Payment complete
            # Update your database, mark the subscription as paid
            # E.g., Subscription.objects.filter(transaction_id=txn_id).update(paid=True)
            logger.info(f"Payment successful for txn: {txn_id}")
            return JsonResponse({'status': 'success', 'message': 'Payment successful'})

        elif status == '-1':  # Payment failed
            # Handle failed payment
            logger.error(f"Payment failed for txn: {txn_id}")
            return JsonResponse({'status': 'error', 'message': 'Payment failed'}, status=400)

        return JsonResponse({'status': 'error', 'message': 'Unhandled IPN status'}, status=400)
