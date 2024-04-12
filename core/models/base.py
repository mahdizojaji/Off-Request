from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    uuid = models.UUIDField(
        verbose_name=_("uuid"),
        default=uuid4,
        unique=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now=True,
    )

    class Meta:
        abstract = True
