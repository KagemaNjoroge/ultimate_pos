# Generated by Django 5.0 on 2024-01-03 10:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0002_customer_kra_pin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="kra_pin",
            field=models.CharField(
                blank=True, default="A000000000Z", max_length=12, null=True
            ),
        ),
    ]
