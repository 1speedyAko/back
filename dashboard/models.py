from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserDashboard(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Dashboard"
