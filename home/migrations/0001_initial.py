# Generated by Django 4.2.7 on 2023-12-05 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('milage', models.CharField(max_length=5)),
                ('transmission', models.CharField(choices=[('Automatic', 'Automatic'), ('Manual', 'Manual')], max_length=20)),
                ('rentAmount', models.IntegerField(default=0)),
                ('color', models.CharField(max_length=30)),
                ('year', models.IntegerField()),
                ('carImg', models.ImageField(upload_to='car_images/')),
                ('fuel', models.CharField(choices=[('Diesel', 'Diesel'), ('Petrol', 'Petrol'), ('Electric', 'Electric')], max_length=20)),
                ('is_available', models.BooleanField(default=True)),
                ('description', models.CharField(max_length=80)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
