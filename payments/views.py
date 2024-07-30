from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
from .utils import create_payment, validate_webhook_signature
from subscriptions.models import UserSubscription
from datetime import timedelta
from django.utils import timezone

class CreateSubscriptionView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product_id')
        amount = request.data.get('amount')
        currency = request.data.get('currency')
        period = request.data.get('period')

        if period == '1_month':
            amount = 49.9
        elif period == '2_months':
            amount = 89.9
        elif period == "3_months":
            amount = 129.9
        else:
            return Response({"error": "Invalid subscription period"}, status=status.HTTP_400_BAD_REQUEST)

        response = create_payment(amount, currency, period)

        if response['state'] == 0:
            payment = Payment.objects.create(
                order_id=response['result']['uuid'],
                user=user,
                product_id=product_id,
                amount=amount,
                currency=currency,
                status='pending',
                transaction_id=response['result']['uuid'],
            )
            return Response(response['result'], status=status.HTTP_201_CREATED)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class CryptomusWebhookView(APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request, *args, **kwargs):
        payload = request.data
        signature = request.headers.get('sign')

        if not validate_webhook_signature(payload, signature):
            return Response({"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

        transaction_id = payload.get('transaction_id')
        webhook_status = payload.get('status')  # Changed to avoid shadowing 'status'

        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
            payment.status = webhook_status
            payment.save()

            if webhook_status == 'confirmed':
                user_subscription, created = UserSubscription.objects.get_or_create(user=payment.user)
                if created:
                    user_subscription.start_date = timezone.now()

                if payload['period'] == '1_month':
                    user_subscription.end_date = user_subscription.start_date + timedelta(days=30)
                elif payload['period'] == '2_months':
                    user_subscription.end_date = user_subscription.start_date + timedelta(days=60)
                elif payload['period'] == '3_months':
                    user_subscription.end_date = user_subscription.start_date + timedelta(days=90)
                
                user_subscription.status = 'active'
                user_subscription.save()

            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_400_BAD_REQUEST)
        except UserSubscription.DoesNotExist:
            return Response({'error': 'User subscription not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
