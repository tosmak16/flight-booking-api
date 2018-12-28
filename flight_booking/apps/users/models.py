from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager)
from django.contrib.auth.hashers import make_password
from django.utils import timezone

class UserManager(BaseUserManager):

    def create_user(self, email, password=None):

        if email is None:
            raise ValueError("Email is required")

        user = self.model(
            email=self.normalize_email(email),
            password=make_password(password))
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.IntegerField(blank=True, default=0)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    passport_url = models.FileField(default='')

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'@{self.email}'

    def get_short_name(self):
        return self.last_name

    def get_long_name(self):
        return f'{self.last_name} @{self.first_name}'