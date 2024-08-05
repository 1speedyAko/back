# subscriptions/urls.py
from django.urls import path
from .views import SubscriptionPlanListView, UserSubscriptionView

urlpatterns = [
    path('plans/', SubscriptionPlanListView.as_view(), name='subscription-plans'),
    path('user-subscription/', UserSubscriptionView.as_view(), name='user-subscription'),
]
