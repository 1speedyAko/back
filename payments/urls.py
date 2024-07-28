from django.urls import path
from .views import create_payment, payment_callback, check_payment_status

urlpatterns = [
    path('create-payment/', create_payment, name='create_payment'),
    path('payment-callback/', payment_callback, name='payment_callback'),
    path('check-payment-status/', check_payment_status, name='check_payment_status'),
]
