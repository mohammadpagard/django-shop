from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.utils import timezone
from django.contrib import messages


# Customizing user model
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=80)
    phone_number = models.CharField(max_length=11, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'full_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(default=timezone.now)
    # expired = models.DateTimeField(default=timezone.)

    def __str__(self):
        return self.phone_number
