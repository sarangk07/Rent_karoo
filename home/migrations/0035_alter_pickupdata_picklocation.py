# Generated by Django 4.2.7 on 2023-12-27 04:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0034_pickupdata_picklocation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pickupdata",
            name="PickLocation",
            field=models.CharField(
                choices=[("Kozhikode", "Kozhikode")], default="", max_length=20
            ),
        ),
    ]