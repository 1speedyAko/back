from rest_framework import generics, permissions
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from .models import SubscriptionPlan, UserSubscription
from .serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer
from django.utils import timezone
from payments.coinpayments import CoinPaymentsAPI
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from datetime import timedelta
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

# List all available subscription plans
class SubscriptionPlanListView(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.IsAuthenticated]


# List the current user's subscriptions
class UserSubscriptionListView(generics.ListAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserSubscription.objects.filter(user=self.request.user)


# Handle subscription creation and redirect to payment URL
class CreateSubscriptionPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, plan_name):
        try:
            # Log incoming request data for debugging
            logger.info(f"Received subscription request: {request.data}")

            # Retrieve the subscription plan
            plan = get_object_or_404(SubscriptionPlan, category=plan_name)
            amount = plan.price
            email = request.user.email

            # Create payment
            coinpayments = CoinPaymentsAPI()
            payment_response = coinpayments.create_payment(amount, plan.currency, email, plan.category)

            if payment_response.get('error') == 'ok':
                payment_url = payment_response['result']['checkout_url']
                return JsonResponse({'payment_url': payment_url})
            else:
                logger.error(f"Payment error: {payment_response.get('error')}")
                return JsonResponse({'status': 'error', 'message': payment_response.get('error')}, status=400)

        except SubscriptionPlan.DoesNotExist:
            logger.error("Subscription plan not found.")
            return JsonResponse({'status': 'error', 'message': 'Subscription plan not found'}, status=404)
        except Exception as e:
            logger.exception("An unexpected error occurred.")
            return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)
        
# Handle CoinPayments webhook for payment confirmation
@csrf_exempt
def coinpayments_webhook(request):
    if request.method == 'POST':
        hmac_header = request.META.get('HTTP_HMAC')
        ipn_data = request.POST.dict()

        coinpayments = CoinPaymentsAPI()

        # Validate the IPN data from CoinPayments
        if coinpayments.validate_ipn(hmac_header, ipn_data):
            status = ipn_data.get('status')
            plan_name = ipn_data.get('custom')  # Plan name (sent in custom field)
            buyer_email = ipn_data.get('buyer_email')

            if status == '100':  # Payment completed successfully
                try:
                    # Fetch user and plan details
                    user = User.objects.get(email=buyer_email)
                    plan = SubscriptionPlan.objects.get(category=plan_name)

                    # Update or create user subscription
                    subscription, created = UserSubscription.objects.get_or_create(user=user, plan=plan)

                    # Set subscription duration based on plan
                    subscription.start_date = timezone.now()
                    subscription.end_date = timezone.now() + timedelta(days=30 * plan.duration_in_months)
                    subscription.status = 'active'
                    subscription.save()

                    return HttpResponse('IPN received and subscription updated', status=200)

                except (User.DoesNotExist, SubscriptionPlan.DoesNotExist):
                    return HttpResponse('Invalid user or subscription plan', status=400)

        return HttpResponse('Invalid IPN', status=400)

    return HttpResponse('Invalid request method', status=400)
