# Generated by Django 4.2.7 on 2023-12-21 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_alter_pickupdata_options_pickupdata_pay'),
    ]

    operations = [
        migrations.AddField(
            model_name='pickupdata',
            name='bookedDate',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
