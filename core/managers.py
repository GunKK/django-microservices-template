from django.contrib.auth.models import BaseUserManager
from django.db import models

from .querysets import  UserQuerySet


class UserManager(BaseUserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username.lower(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("role", 1)

        return self.create_user(username, password, **extra_fields)
