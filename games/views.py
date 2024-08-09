from rest_framework import generics,permissions
from .models import Game
from .serializers import GameSerializer

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
        if user.is_premium:
            return Game.objects.filter(is_premium = True)
        return Game.objects.none()