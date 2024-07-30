from rest_framework import serializers
from .models import SubscriptionPlan,UserSubscription

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'


class UserSubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = '__all__'