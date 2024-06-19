from django.db import models

from customers.models import Customer
from products.models import Product


class SaleItem(models.Model):
    product = models.ForeignKey(
        Product, models.CASCADE, db_column="product", related_name="sale_items"
    )
    quantity = models.IntegerField(default=1)

    class Meta:

        verbose_name_plural = "Sale Items"
        verbose_name = "Sale Item"

    def __str__(self) -> str:
        return f"{self.product.name} - {self.quantity}"

    def total(self):
        return self.product.price * self.quantity


class Sale(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(
        Customer,
        models.SET_NULL,
        db_column="customer",
        blank=True,
        null=True,
        related_name="sales",
    )
    items = models.ManyToManyField(SaleItem)
    sub_total = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    total_tax_amount = models.FloatField(default=0)
    amount_paid = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    # if printed add a watermark to the receipt
    receipt_is_printed = models.BooleanField(default=False)

    class Meta:

        verbose_name_plural = "Sales"
        verbose_name = "Sale"

    def __str__(self) -> str:
        return str(self.id)

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "date_added": self.date_added,
            "customer": self.customer.get_full_name(),
            "sub_total": self.sub_total,
            "grand_total": self.grand_total,
            "tax_amount": self.tax_amount,
            "tax_percentage": self.tax_percentage,
            "amount_paid": self.amount_payed,
            "amount_change": self.amount_change,
            "receipt_is_printed": self.receipt_is_printed,
        }
