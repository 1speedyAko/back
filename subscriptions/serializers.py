from rest_framework import serializers
from .models import SubscriptionPlan, UserSubscription,Payment

# Serializer for the SubscriptionPlan model
class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['category', 'price', 'currency', 'description',  'info_1', 'info_2','discount']

# Serializer for the UserSubscription model
class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer(read_only=True)  # Nested serializer for plan details
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = UserSubscription
        fields = ['user', 'plan', 'start_date', 'end_date', 'status', 'is_active']

    def get_is_active(self, obj):
        return obj.is_active()  # Return whether the subscription is active or not

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
