# Generated by Django 4.2.7 on 2023-12-20 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_alter_cars_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='cars',
            name='stock',
            field=models.IntegerField(default=0),
        ),
    ]