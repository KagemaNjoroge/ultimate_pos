# Generated by Django 5.0.2 on 2024-03-08 09:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0009_alter_customer_photo'),
        ('sales', '0013_sale_receipt_is_printed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='customer',
            field=models.ForeignKey(blank=True, db_column='customer', null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.customer'),
        ),
    ]
