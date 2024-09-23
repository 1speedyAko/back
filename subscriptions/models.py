from django.db import models
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
    
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        default='silver', 
        blank=True
    )
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False, null=False)
    currency = models.CharField(max_length=3, default='USD')
    description = models.CharField(max_length=255, blank=False, null=False)
    discount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # Made optional
    duration_in_months = models.PositiveIntegerField(default=1)  # New field
    info_1 = models.CharField(max_length=30, blank=True,null=True)
    info_2 = models.CharField(max_length=30, blank=True,null=True)
    def __str__(self):
        return f"{self.category.capitalize()} Plan"



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

    def is_active(self):
        return self.status == 'active' and self.end_date > timezone.now()

    def __str__(self):
        return f"{self.user.email} - {self.plan.category.capitalize()} Subscription"

    @classmethod
    def user_has_active_subscription(cls, user):
        return cls.objects.filter(user=user, status='active', end_date__gt=timezone.now()).exists()
        
    def save(self, *args, **kwargs):
        if not self.end_date:
            if self.plan.category == 'silver':
                self.end_date = self.start_date + timedelta(days=30 * self.plan.duration_in_months)
            elif self.plan.category == 'gold':
                self.end_date = self.start_date + timedelta(days=30 * self.plan.duration_in_months)
            elif self.plan.category == 'platinum':
                self.end_date = self.start_date + timedelta(days=30 * self.plan.duration_in_months)
        super().save(*args, **kwargs)