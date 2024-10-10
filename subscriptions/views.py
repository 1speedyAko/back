from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SubscriptionPlan, UserSubscription, Payment
from .serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer
from .binance_service import BinancePaymentService
import time
import hmac
import hashlib
import logging

logger = logging.getLogger(__name__)

class SubscriptionPlanListView(APIView):
    def get(self, request):
        plans = SubscriptionPlan.objects.all()
        serializer = SubscriptionPlanSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateSubscriptionView(APIView):
    def post(self, request, plan_name):
        try:
            plan = SubscriptionPlan.objects.get(category=plan_name.lower())
            order_id = f"{request.user.id}-{int(time.time())}"
            
            # Create payment entry with 'pending' status
            payment = Payment.objects.create(
                user=request.user,
                amount=plan.price,
                currency=plan.currency,
                status='pending',
                order_id=order_id
            )

            # Generate payment link via BinancePaymentService
            binance_service = BinancePaymentService()
            payment_url = binance_service.create_payment(order_id, plan.price, plan.currency)

            if not payment_url:
                return Response({"error": "Failed to generate payment link"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"payment_url": payment_url}, status=status.HTTP_201_CREATED)

        except SubscriptionPlan.DoesNotExist:
            return Response({"error": "Subscription plan not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in subscription creation: {e}")
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BinanceIPNView(APIView):
    def post(self, request):
        # Verify Binance's IPN signature
        received_signature = request.headers.get("Binance-IPN-Signature")
        payload = request.body

        # Generate the HMAC SHA256 signature
        secret = settings.BINANCE_API_SECRET.encode()
        calculated_signature = hmac.new(secret, payload, hashlib.sha256).hexdigest()

        if calculated_signature != received_signature:
            logger.warning("Invalid IPN signature received.")
            return Response({"error": "Invalid signature"}, status=status.HTTP_403_FORBIDDEN)

        transaction_id = request.data.get("transaction_id")
        order_id = request.data.get("merchant_order_id")
        status = request.data.get("status")

        if not all([transaction_id, order_id, status]):
            logger.error("Incomplete IPN data received.")
            return Response({"error": "Incomplete data"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = Payment.objects.get(order_id=order_id)
            payment.status = "confirmed" if status == "SUCCESS" else "failed"
            payment.transaction_id = transaction_id
            payment.save()
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            logger.error(f"Payment with order_id {order_id} not found.")
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
