from django.urls import path
from .views import create_subscription, coinpayments_webhook

urlpatterns = [
    path('create-subscription/', create_subscription, name='create-subscription'),
    path('webhook/', coinpayments_webhook, name='coinpayments-webhook'),
]
