
from rest_framework import serializers
from .models import Game, Announcement

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['match','odd','time','pick','is_premium']

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'