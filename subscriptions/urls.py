from django.urls import path
from .views import (
    SubscriptionPlanListView,
    UserSubscriptionListView,
    CreateSubscriptionPaymentView,  # Updated to use class-based view
    coinpayments_webhook,
)

urlpatterns = [
    path('plans/', SubscriptionPlanListView.as_view(), name='subscription-plan-list'),
    path('my-subscriptions/', UserSubscriptionListView.as_view(), name='user-subscription-list'),
    path('create/<str:plan_name>/', CreateSubscriptionPaymentView.as_view(), name='create-subscription'),  # Updated to class-based view
    path('coinpayments/webhook/', coinpayments_webhook, name='coinpayments-webhook'),
]
