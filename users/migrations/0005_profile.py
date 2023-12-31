# Generated by Django 4.2.7 on 2023-12-12 07:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_registerinfo_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                ("address", models.CharField(max_length=100)),
                ("mobile", models.BigIntegerField()),
                ("gender", models.CharField(max_length=10)),
                ("age", models.IntegerField()),
                ("education", models.CharField(max_length=50)),
                ("state", models.CharField(max_length=30)),
                ("city", models.CharField(max_length=40)),
                ("profilePic", models.ImageField(upload_to="media/userimages")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
