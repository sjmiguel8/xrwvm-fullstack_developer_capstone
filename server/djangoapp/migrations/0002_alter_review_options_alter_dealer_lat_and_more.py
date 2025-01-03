# Generated by Django 5.1.4 on 2025-01-04 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-purchase_date']},
        ),
        migrations.AlterField(
            model_name='dealer',
            name='lat',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='long',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='short_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='st',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='review',
            name='car_year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
