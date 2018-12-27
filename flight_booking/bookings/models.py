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