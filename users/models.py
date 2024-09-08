from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    _is_staff = models.BooleanField(default=False)  # Internal field for is_staff
    is_superuser = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        """
        All superusers are staff by default, but we also allow regular users to be staff.
        """
        return self.is_superuser or self._is_staff

    @is_staff.setter
    def is_staff(self, value):
        """
        Allow explicitly setting the staff status for regular users.
        """
        self._is_staff = value

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser 

   

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)