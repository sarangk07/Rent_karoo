# Generated by Django 4.2.7 on 2023-12-06 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cars',
            name='carImg',
            field=models.ImageField(upload_to='templates/garage/car_images/'),
        ),
    ]