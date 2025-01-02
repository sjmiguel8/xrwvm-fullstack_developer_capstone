# Generated by Django 5.1.4 on 2025-01-02 23:37

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarDealer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='CarMake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Dealer',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('st', models.CharField(max_length=2)),
                ('address', models.CharField(max_length=100)),
                ('zip', models.CharField(max_length=10)),
                ('lat', models.FloatField(default=0.0)),
                ('long', models.FloatField(default=0.0)),
                ('short_name', models.CharField(default='', max_length=100)),
                ('full_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('car_type', models.CharField(choices=[('SEDAN', 'Sedan'), ('SUV', 'SUV'), ('WAGON', 'Wagon'), ('SPORT', 'Sport'), ('COUPE', 'Coupe'), ('MINIVAN', 'Mini Van')], max_length=10)),
                ('year', models.IntegerField(validators=[django.core.validators.MinValueValidator(2015), django.core.validators.MaxValueValidator(2023)])),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('car_make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.carmake')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('review', models.TextField()),
                ('purchase', models.BooleanField(default=False)),
                ('purchase_date', models.DateField(blank=True, null=True)),
                ('car_make', models.CharField(max_length=100)),
                ('car_model', models.CharField(max_length=100)),
                ('car_year', models.IntegerField()),
                ('dealership', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.dealer')),
            ],
        ),
    ]
