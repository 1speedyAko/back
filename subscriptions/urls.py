# subscriptions/urls.py
from django.urls import path
from .views import SubscriptionPlanListView, UserSubscriptionListView

urlpatterns = [
    path('plans/', SubscriptionPlanListView.as_view(), name='subscription-plans'),
    path('user-subscription/', UserSubscriptionListView.as_view(), name='user-subscription'),
]
