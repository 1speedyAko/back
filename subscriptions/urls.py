# subscriptions/urls.py

from django.urls import path
from .views import SubscriptionView

urlpatterns = [
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
]
