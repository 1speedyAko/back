from django.urls import path
from .views import SubscriptionPlanListView, CreateSubscriptionView, BinanceIPNView

urlpatterns = [
    path('plans/', SubscriptionPlanListView.as_view(), name='subscription-plans'),
    path('create/<str:plan_name>/', CreateSubscriptionView.as_view(), name='create-subscription'),
    path('binance-ipn/', BinanceIPNView.as_view(), name='binance-ipn'),
]
