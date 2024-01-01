# Generated by Django 4.2.7 on 2023-12-27 04:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0033_pickupdata_plan"),
    ]

    operations = [
        migrations.AddField(
            model_name="pickupdata",
            name="PickLocation",
            field=models.CharField(
                choices=[
                    ("Silver", "Silver"),
                    ("Gold", "Gold"),
                    ("Diamond", "Diamond"),
                ],
                default="",
                max_length=20,
            ),
        ),
    ]