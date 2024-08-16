from django.urls import path
from .views import CreateSubscriptionView, CryptomusWebhookView, CheckPaymentStatusView

urlpatterns = [
    path('create-subscription/', CreateSubscriptionView.as_view(), name='create_subscription'),
    path('webhook/', CryptomusWebhookView.as_view(), name='cryptomus_webhook'),
    path('check-payment-status/', CheckPaymentStatusView.as_view(), name='check_payment_status'),
]
