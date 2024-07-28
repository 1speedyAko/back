from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Payment
from .serializers import PaymentSerializer
from .utils import initiate_payment, verify_payment

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=['post'])
    def create_payment(self, request):
        data = request.data
        user = request.user
        product_id = data.get('product_id')
        amount = data.get('amount')
        currency = data.get('currency')

        # Initiate payment
        payment_response = initiate_payment(user, product_id, amount, currency)
        
        if payment_response['status'] == 'success':
            payment = Payment.objects.create(
                user=user,
                product_id=product_id,
                amount=amount,
                currency=currency,
                order_id=payment_response['order_id'],
                transaction_id=payment_response['transaction_id'],
                status='pending'
            )
            return Response({'status': 'success', 'payment': PaymentSerializer(payment).data})
        else:
            return Response({'status': 'failed', 'message': payment_response['message']}, status=400)

    @action(detail=False, methods=['post'])
    def verify_payment(self, request):
        order_id = request.data.get('order_id')
        payment = Payment.objects.get(order_id=order_id)

        # Verify payment
        verification_response = verify_payment(payment)

        if verification_response['status'] == 'confirmed':
            payment.status = 'confirmed'
            payment.save()
            return Response({'status': 'success', 'payment': PaymentSerializer(payment).data})
        else:
            payment.status = 'failed'
            payment.save()
            return Response({'status': 'failed', 'message': verification_response['message']}, status=400)
