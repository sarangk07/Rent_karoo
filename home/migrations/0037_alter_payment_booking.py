# Generated by Django 4.2.7 on 2024-01-01 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0036_pickupdata_totalamt"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="booking",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="home.pickupdata",
            ),
        ),
    ]