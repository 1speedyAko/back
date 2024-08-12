from rest_framework import generics,permissions
from .models import Game
from .serializers import GameSerializer
from django.utils import timezone
from subscriptions.models import UserSubscription

class FreeOddsListView(generics.ListAPIView):
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        return Game.objects.filter(is_premium=False)
    




class PremiumPicksListView(generics.ListAPIView):
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        has_active_subscription = UserSubscription.user_has_active_subscription(user)
        print(f"User: {user}, Has Active Subscription: {has_active_subscription}")

        if has_active_subscription:
            return Game.objects.filter(is_premium=True)
        return Game.objects.none()
        


        
