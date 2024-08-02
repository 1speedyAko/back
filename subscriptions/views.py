# subscriptions/views.py

from rest_framework import generics, permissions
from .models import SubscriptionPlan, UserSubscription
from .serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer

class SubscriptionPlanListView(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]

class UserSubscriptionView(generics.RetrieveAPIView):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.queryset.get(user=self.request.user)
