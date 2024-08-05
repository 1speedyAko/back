# games/views.py
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Game
from .serializers import GameSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == 'premium_odds':
            return Game.objects.filter(is_premium=True)
        return super().get_queryset()

    @action(detail=False, methods=['get'])
    def premium_odds(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
