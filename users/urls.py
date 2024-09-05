from django.urls import path, include
from .views import LogoutView, UserDetailView

urlpatterns = [
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
]
