# subscriptions/models.py

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()

class SubscriptionPlan(models.Model):
    CATEGORY_CHOICES = [
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ]
    
    CURRENCY_CHOICES = [
        ('USDC', 'USDC'),
        ('USDT', 'USDT'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='silver', blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='USDC')
    description = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    duration_in_months = models.PositiveIntegerField(default=1)
    info_1 = models.CharField(max_length=30, blank=True, null=True)
    info_2 = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"{self.category.capitalize()} Plan - {self.currency}"


class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=30 * self.plan.duration_in_months)
        super().save(*args, **kwargs)

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed'),
    ]

    order_id = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, choices=[('USDC', 'USDC'), ('USDT', 'USDT')])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.amount} {self.currency} - {self.status}"
