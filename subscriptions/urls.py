from django.urls import path
from .views import (
    SubscriptionPlanListView,
    UserSubscriptionListView,
    create_subscription_payment,
    coinpayments_webhook,
)

urlpatterns = [
    path('plans/', SubscriptionPlanListView.as_view(), name='subscription-plan-list'),
    path('my-subscriptions/', UserSubscriptionListView.as_view(), name='user-subscription-list'),
    path('subscriptions/create/<str:plan_name>/', create_subscription_payment, name='create-subscription'),
    path('coinpayments/webhook/', coinpayments_webhook, name='coinpayments-webhook'),
]
