from rest_framework import generics, permissions
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import SubscriptionPlan, UserSubscription
from .serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer
from django.utils import timezone
from payments.coinpayments import CoinPaymentsAPI
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from datetime import timedelta

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

coinpayments = CoinPaymentsAPI()

# Handle subscription creation and redirect to payment URL
def create_subscription_payment(request, plan_name):
    plan = SubscriptionPlan.objects.get(name=plan_name)

    if request.method == 'POST':
        # Get the plan's price and the user's email
        amount = plan.price
        email = request.user.email

        # Create the payment using CoinPayments API
        payment_response = coinpayments.create_payment(amount, 'USD', email, plan_name)

        if payment_response.get('error') == 'ok':
            # Get the payment URL (might include a QR code or redirect link)
            payment_url = payment_response['result']['checkout_url']
            return JsonResponse({'payment_url': payment_url})
        else:
            return JsonResponse({'status': 'error', 'message': payment_response.get('error')})

    return render(request, 'subscription_payment.html', {'plan': plan})

# Handle CoinPayments webhook for payment confirmation
@csrf_exempt
def coinpayments_webhook(request):
    if request.method == 'POST':
        hmac_header = request.META.get('HTTP_HMAC')
        ipn_data = request.body.decode()

        coinpayments = CoinPaymentsAPI()

        # Validate the IPN data from CoinPayments
        if coinpayments.validate_ipn(hmac_header, ipn_data):
            status = request.POST.get('status')
            custom = request.POST.get('custom')  # Plan name
            buyer_email = request.POST.get('buyer_email')
            
            if status == '100':  # Payment completed successfully
                user = User.objects.get(email=buyer_email)
                plan = SubscriptionPlan.objects.get(name=custom)
                
                # Update or create user subscription
                subscription, created = UserSubscription.objects.get_or_create(user=user)
                subscription.plan = plan
                subscription.end_date = timezone.now() + timedelta(days=30 * plan.duration_in_months)
                subscription.save()

                return HttpResponse('IPN received', status=200)
    
    return HttpResponse('Invalid IPN', status=400)
