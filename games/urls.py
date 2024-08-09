# games/urls.py

from django.urls import path, include
from .views import FreeOddsListView, PremiumPicksListView

urlpatterns = [
    path('free-odds/', FreeOddsListView.as_view(), name='free-odds'),
    path('premium-picks/', PremiumPicksListView.as_view(), name='premium-picks'),
]
