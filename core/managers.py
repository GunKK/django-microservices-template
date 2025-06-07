from django.contrib.auth.models import BaseUserManager
from .querysets import UserQuerySet


class SoftDeleteUserManager(BaseUserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username.lower(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("role", 1)

        return self.create_user(username, password, **extra_fields)


class GlobalUserManager(BaseUserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)


class DeletedUserManager(BaseUserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db).filter(deleted_at__isnull=False)
