import uuid
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_softdelete.models import SoftDeleteModel
from .managers import DeletedUserManager, GlobalUserManager, SoftDeleteUserManager

from core.constant import USER_DEFAULT_SYSTEM, NotificationTypeEnum

class User(AbstractBaseUser, TimeStampedModel, SoftDeleteModel):
    username = models.CharField(unique=True, null=True, max_length=255)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    role = models.IntegerField(default=1)
    avatar = models.ImageField(
        upload_to="avatar/",
        blank=True,
        default=None,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])
        ],
        max_length=255,
    )
    status = models.BooleanField(default=True)

    objects = SoftDeleteUserManager()
    global_objects = GlobalUserManager()
    deleted_objects = DeletedUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "role", "password"]

    token_version = models.UUIDField(default=uuid.uuid4)

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.pk} {self.username}"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def set_new_token_version(self):
        """
        Set a new token version (UUID) for the User.
        """
        self.token_version = uuid.uuid4()
        self.save()

    def get_new_token_version(self) -> str:
        """
        Get a new token version (UUID) for the User.
        """
        return str(self.token_version)

    def is_token_version_valid(self, token_version: str) -> bool:
        return bool(self.get_new_token_version() == token_version)


class Notification(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, default=USER_DEFAULT_SYSTEM, null=True
    )
    notify_type = models.IntegerField(
        default=NotificationTypeEnum.SYSTEM_NOTIFICATION.value
    )
    data = models.JSONField(null=True, blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.full_name} - {self.notify_type}"

    class Meta:
        db_table = "notifications"
        ordering = ["-created"]
