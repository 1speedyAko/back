from rest_framework import serializers
from .models import UserDashboard

class UserDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDashboard
        fields = '__all__'
