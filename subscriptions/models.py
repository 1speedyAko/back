from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


from django.db import models

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
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False, null=False)  # Store price with two decimal places
    currency = models.CharField(max_length=3, default='USD')  # Currency code, e.g., 'USD'
    description = models.CharField(max_length=255, blank=False, null=False)  # Description of the plan
    discount = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)  # Optional discount
    
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
        return f"{self.user.email} - "

    @classmethod
    def user_has_active_subscription(cls, user):
        return cls.objects.filter(user=user, status='active', end_date__gt=timezone.now()).exists()
        
    def save(self, *args, **kwargs):
        if not self.end_date:
            if self.plan.category == 'silver':
                self.end_date = self.start_date + timedelta(days=30)
            elif self.plan.category == 'gold':
                self.end_date = self.start_date + timedelta(days=60)
            elif self.plan.category == 'platinum':
                self.end_date = self.start_date + timedelta(days=90)
        super().save(*args, **kwargs)


