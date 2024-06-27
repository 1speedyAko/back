# payments/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, CoinPaymentsWebhookView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create-charge/', PaymentViewSet.as_view({'post': 'create_charge'}), name='create_charge'),
    path('webhook/', CoinPaymentsWebhookView.as_view(), name='coinpayments_webhook'),
]
