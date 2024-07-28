from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .cryptomus import CryptomusAPI
from django.conf import settings

@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        data = request.json()
        try:
            amount = data['amount']
            currency = data['currency']
            order_id = data['order_id']
            callback_url = data['callback_url']
        except KeyError:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        cryptomus = CryptomusAPI(settings.CRYPTO_API_KEY, settings.CRYPTO_SECRET_KEY)
        response = cryptomus.create_invoice(amount, currency, order_id, callback_url)
        
        if response.get('error'):
            return JsonResponse({'error': response['error']}, status=400)

        Payment.objects.create(
            order_id=order_id,
            amount=amount,
            currency=currency,
            status='pending'
        )

        return JsonResponse(response)

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        if not verify_signature(request):
            return JsonResponse({'status': 'failed', 'message': 'Invalid signature'}, status=400)

        data = request.json()
        try:
            order_id = data['order_id']
            status = data['status']
        except KeyError:
            return JsonResponse({'status': 'failed', 'message': 'Missing order_id or status'}, status=400)

        try:
            payment = Payment.objects.get(order_id=order_id)
            payment.status = status
            payment.save()
        except Payment.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Payment not found'}, status=404)

        return JsonResponse({'status': 'success'})


@csrf_exempt
def check_payment_status(request):
    if request.method == 'POST':
        data = request.json()
        order_id = data['order_id']

        cryptomus = CryptomusAPI(settings.CRYPTO_API_KEY, settings.CRYPTO_SECRET_KEY)
        response = cryptomus.check_payment_status(order_id)
        
        # Update payment status in the database
        try:
            payment = Payment.objects.get(order_id=order_id)
            payment.status = response['status']
            payment.save()
        except Payment.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Payment not found'}, status=404)

        return JsonResponse(response)
