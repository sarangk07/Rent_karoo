# Generated by Django 4.2.7 on 2023-12-16 03:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0017_wishlist"),
    ]

    operations = [
        migrations.AddField(
            model_name="wishlist",
            name="wishlist_items",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
