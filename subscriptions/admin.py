from django.contrib import admin
from .models import SubscriptionPlan,UserSubscription

admin.site.register(SubscriptionPlan)
admin.site.register(UserSubscription)