from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

from core.models.base import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not phone_number:
            raise ValueError(_("The phone_number must be set"))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(phone_number, password, **extra_fields)


class User(BaseModel, AbstractUser):
    username = None
    objects = UserManager()
    phone_number = models.CharField(
        verbose_name=_("phone number"),
        unique=True,
    )

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
