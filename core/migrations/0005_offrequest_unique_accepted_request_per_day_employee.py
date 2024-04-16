# Generated by Django 5.0.3 on 2024-04-16 21:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_alter_offrequest_state"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="offrequest",
            constraint=models.UniqueConstraint(
                condition=models.Q(("state", "RJCT"), _negated=True),
                fields=("off_at", "state", "employee"),
                name="unique_accepted_request_per_day_employee",
            ),
        ),
    ]