from django.urls import path
from .views import create_subscription, CoinPaymentsIPNView

urlpatterns = [
    # URL for creating the subscription
    path('create-subscription/', create_subscription, name='create_subscription'),
    
    # URL for handling IPN from CoinPayments
    path('ipn-handler/', CoinPaymentsIPNView.as_view(), name='coinpayments_ipn'),
]
