from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from core.models import User
from core.models.base import BaseModel


class OffRequest(BaseModel):
    class State(models.TextChoices):
        TEMP = "TEMP", _("موقت")
        EMPLOYER_WAITING = "EMPW", _("در انتظار تایید کارفرما")
        ACCEPTED = "ACPT", _("تایید شده")
        REJECTED = "RJCT", _("رد شده")

    state = models.CharField(
        verbose_name=_("state"),
        choices=State.choices,
        default=State.TEMP,
    )
    off_at = models.DateField(
        verbose_name=_("off date"),
        null=True,
        blank=True,
    )
    employee = models.ForeignKey(
        verbose_name=_("employee"),
        to=User,
        on_delete=models.CASCADE,
        related_name="off_requests",
    )
    reject_reason = models.TextField(
        verbose_name=_("reject reason"),
        blank=True,
    )

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = _("off request")
        verbose_name_plural = _("off requests")
        constraints = [
            models.UniqueConstraint(
                fields=["off_at", "state", "employee"],
                name="unique_accepted_request_per_day_employee",
                condition=~Q(state="RJCT"),
            ),
        ]
