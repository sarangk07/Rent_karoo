# Generated by Django 4.2.7 on 2023-12-20 09:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0026_remove_cars_stock_stock"),
    ]

    operations = [
        migrations.RenameField(
            model_name="stock",
            old_name="stock",
            new_name="quantity",
        ),
    ]
