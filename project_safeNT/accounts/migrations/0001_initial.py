# Generated by Django 5.1.2 on 2024-11-02 16:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
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
                    "role",
                    models.CharField(
                        choices=[
                            ("CITIZEN", "Citizen"),
                            ("POLICE", "Police"),
                            ("DOCTOR", "Doctor"),
                            ("PENDING", "Pending"),
                        ],
                        default="CITIZEN",
                        max_length=10,
                    ),
                ),
                (
                    "intended_role",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("CITIZEN", "Citizen"),
                            ("POLICE", "Police"),
                            ("DOCTOR", "Doctor"),
                            ("PENDING", "Pending"),
                        ],
                        max_length=10,
                        null=True,
                    ),
                ),
                ("phone_number", models.CharField(max_length=17)),
                ("address", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
