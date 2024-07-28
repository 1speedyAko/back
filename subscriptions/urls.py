from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionPlanViewSet, UserSubscriptionViewSet, process_payment

router = DefaultRouter()
router.register(r'plans', SubscriptionPlanViewSet)
router.register(r'user-subscriptions', UserSubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('process-payment/', process_payment, name='process-payment'),
]
