from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email , password , **extrafields):

        extrafields.setdefault('is_staff',True)
        extrafields.setdefault('is_superuser',True)
        extrafields.setdefault('is_active',True)

        if extrafields.get('is_staff') is not True:
            raise ValueError(_("superuser must have staff=True"))
        if extrafields.get('is_superuser') is not True:
            raise ValueError(_("superuser must have superuser=True"))
        return self.create_user(email, password , **extrafields)