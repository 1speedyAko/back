from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserDashboard
from rest_framework import viewsets
from .serializers import UserDashboardSerializer

class UserDashboardViewSet(viewsets.ModelViewSet):
    queryset = UserDashboard.objects.all()
    serializer_class = UserDashboardSerializer

    @action(detail=False, methods=['get'])
    def my_dashboard(self, request):
        user_dashboard = UserDashboard.objects.get(user=request.user)
        serializer = self.get_serializer(user_dashboard)
        return Response(serializer.data)
