# Generated by Django 4.2.7 on 2024-01-02 05:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0010_remove_registerinfo_block"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="is_block",
            field=models.BooleanField(default=False),
        ),
    ]
