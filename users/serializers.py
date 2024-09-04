from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'password')  
class CustomUserSerializer(UserSerializer):
    is_premium = serializers.BooleanField(read_only=True)
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'is_premium')  
