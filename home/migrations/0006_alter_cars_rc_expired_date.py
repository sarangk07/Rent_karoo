# Generated by Django 4.2.7 on 2023-12-11 05:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0005_cars_carnumber_cars_engine_cars_rc_expired_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cars",
            name="rc_expired_date",
            field=models.CharField(default="", max_length=20),
        ),
    ]
