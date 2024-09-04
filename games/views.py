from rest_framework import generics,permissions
from .models import Game, Announcement
from .serializers import GameSerializer,AnnouncementSerializer
from rest_framework.response import Response
from subscriptions.models import UserSubscription
from rest_framework.views import APIView

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
        


        
class AnnouncementView(APIView):
    def get(self):
        announcements = Announcement.objects.all()
        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)