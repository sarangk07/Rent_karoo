# Generated by Django 4.2.7 on 2023-12-18 10:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0020_remove_wishlist_wish_car_wishlist_wish_car"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cars",
            name="description",
            field=models.CharField(max_length=200),
        ),
    ]
