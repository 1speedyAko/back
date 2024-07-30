from django.urls import path
from .views import CreateSubscriptionView, CryptomusWebhookView

urlpatterns = [
    path('create-subscription/', CreateSubscriptionView.as_view(), name='create_subscription'),
    path('webhook/', CryptomusWebhookView.as_view(), name='cryptomus_webhook'),
]
