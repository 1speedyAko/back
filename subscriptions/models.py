from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


class SubscriptionPlan(models.Model):
    CATEGORY_CHOICES = [
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Silver', blank=True)

    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def is_active(self):
        return self.status == 'active' and self.end_date > timezone.now()

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

    def save(self, *args, **kwargs):
        if not self.end_date:
            if self.plan.category == 'silver':
                self.end_date = self.start_date + timedelta(days=30)
            elif self.plan.category == 'gold':
                self.end_date = self.start_date + timedelta(days=60)
            elif self.plan.category == 'platinum':
                self.end_date = self.start_date + timedelta(days=90)
        super().save(*args, **kwargs)

