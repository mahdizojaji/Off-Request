# Generated by Django 5.0.3 on 2024-04-14 16:16

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_balemessengeruser_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="balemessengeruser",
            name="employee_profile",
            field=models.OneToOneField(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="bale_profile",
                to=settings.AUTH_USER_MODEL,
                verbose_name="employee profile",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="is_employee",
            field=models.BooleanField(default=True, verbose_name="employee status"),
        ),
        migrations.CreateModel(
            name="OffRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, unique=True, verbose_name="uuid"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="created at"),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("TEMP", "Temp"),
                            ("EMPW", "Employer waiting"),
                            ("ACPT", "Accept"),
                            ("RJCT", "Reject"),
                        ],
                        default="TEMP",
                        verbose_name="state",
                    ),
                ),
                (
                    "off_at",
                    models.DateField(blank=True, null=True, verbose_name="off date"),
                ),
                (
                    "reject_reason",
                    models.TextField(blank=True, verbose_name="reject reason"),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="off_requests",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="employee",
                    ),
                ),
            ],
            options={
                "verbose_name": "off request",
                "verbose_name_plural": "off requests",
            },
        ),
    ]
