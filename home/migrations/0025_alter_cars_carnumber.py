# Generated by Django 4.2.7 on 2023-12-20 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_cars_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cars',
            name='carNumber',
            field=models.CharField(default='', max_length=20, unique=True),
        ),
    ]