# Generated by Django 5.0.6 on 2024-06-16 18:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('sub_total', models.FloatField(default=0)),
                ('grand_total', models.FloatField(default=0)),
                ('tax_amount', models.FloatField(default=0)),
                ('tax_percentage', models.FloatField(default=0)),
                ('amount_payed', models.FloatField(default=0)),
                ('amount_change', models.FloatField(default=0)),
                ('receipt_is_printed', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(blank=True, db_column='customer', null=True, on_delete=django.db.models.deletion.SET_NULL, to='customers.customer')),
            ],
            options={
                'verbose_name': 'Sale',
                'verbose_name_plural': 'Sales',
                'db_table': 'Sales',
            },
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('product', models.ForeignKey(db_column='product', on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'verbose_name': 'SaleItem',
                'verbose_name_plural': 'SaleItems',
                'db_table': 'SaleItems',
            },
        ),
        migrations.CreateModel(
            name='SaleDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale', models.ForeignKey(db_column='sale', on_delete=django.db.models.deletion.CASCADE, to='sales.sale')),
                ('items', models.ManyToManyField(db_column='items', to='sales.saleitem')),
            ],
            options={
                'verbose_name': 'SaleDetail',
                'verbose_name_plural': 'SaleDetails',
                'db_table': 'SaleDetails',
            },
        ),
    ]
