# Generated by Django 5.0.14 on 2025-06-20 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='discount',
            field=models.FloatField(default=0),
        ),
    ]
