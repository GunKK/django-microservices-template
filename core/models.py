from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_softdelete.models import SoftDeleteModel

from core.constant import RepairFormStatusEnum

from .managers import UserManager


class User(AbstractBaseUser, TimeStampedModel, SoftDeleteModel):
    email = models.EmailField(unique=True, null=True, max_length=255)
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
    status = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "role", "password"]

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()
