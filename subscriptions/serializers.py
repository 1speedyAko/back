from rest_framework import serializers
from .models import SubscriptionPlan, UserSubscription

# Serializer for the SubscriptionPlan model
class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['category', 'price', 'currency', 'description', 'discount']

# Serializer for the UserSubscription model
class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer(read_only=True)  # Nested serializer for plan details
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = UserSubscription
        fields = ['user', 'plan', 'start_date', 'end_date', 'status', 'is_active']

    def get_is_active(self, obj):
        return obj.is_active()  # Return whether the subscription is active or not
