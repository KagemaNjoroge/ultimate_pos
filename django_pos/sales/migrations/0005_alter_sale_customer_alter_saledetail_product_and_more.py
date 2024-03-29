# Generated by Django 5.0 on 2024-01-06 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0003_alter_customer_kra_pin"),
        ("products", "0004_alter_category_options_alter_product_status"),
        ("sales", "0004_alter_sale_customer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sale",
            name="customer",
            field=models.ForeignKey(
                blank=True,
                db_column="customer",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="customers.customer",
            ),
        ),
        migrations.AlterField(
            model_name="saledetail",
            name="product",
            field=models.ForeignKey(
                db_column="product",
                on_delete=django.db.models.deletion.PROTECT,
                to="products.product",
            ),
        ),
        migrations.AlterField(
            model_name="saledetail",
            name="sale",
            field=models.ForeignKey(
                db_column="sale",
                on_delete=django.db.models.deletion.PROTECT,
                to="sales.sale",
            ),
        ),
    ]
