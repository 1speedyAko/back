from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserDashboardViewSet

router = DefaultRouter()
router.register(r'dashboard', UserDashboardViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('my-dashboard/', UserDashboardViewSet.as_view({'get': 'my_dashboard'}), name='my-dashboard'),
]
