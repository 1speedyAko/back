# payments/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.conf import settings
from .models import Payment, Product
from .serializers import PaymentSerializer
from .utils import create_charge
import hmac
import hashlib
import json

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=['post'])
    def create_charge(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        product = Product.objects.get(id=product_id)
        amount = product.price
        currency = request.data.get('currency')
        buyer_email = user.email
        item_name = product.name

        try:
            charge = create_charge(amount, currency, buyer_email, item_name)
            payment = Payment.objects.create(
                user=user,
                product=product,
                amount=amount,
                status='pending',
                transaction_id=charge['txn_id']
            )

            return Response({'checkout_url': charge['checkout_url']}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# payments/views.py (add this to the existing views)
class CoinPaymentsWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        webhook_secret = settings.COINPAYMENTS_API_SECRET
        request_data = json.loads(request.body.decode('utf-8'))
        signature = request.headers.get('HMAC', '')

        computed_signature = hmac.new(webhook_secret.encode('utf-8'), request.body, hashlib.sha512).hexdigest()

        if hmac.compare_digest(signature, computed_signature):
            txn_id = request_data.get('txn_id')
            status = request_data.get('status')
            
            if status == 100:  # Payment confirmed
                payment = Payment.objects.get(transaction_id=txn_id)
                payment.status = 'confirmed'
                payment.save()

                # Activate subscription
                Subscription.objects.create(
                    user=payment.user,
                    product=payment.product,
                    start_date=timezone.now(),
                    end_date=timezone.now() + timedelta(days=30),  # Example: 1 month subscription
                    active=True
                )

            elif status < 0:  # Payment failed
                payment = Payment.objects.get(transaction_id=txn_id)
                payment.status = 'failed'
                payment.save()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
