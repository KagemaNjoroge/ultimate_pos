# Generated by Django 5.0.6 on 2024-07-01 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0003_purchase_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='quantity',
            field=models.FloatField(default=1.0),
        ),
    ]