from django.db import models

from customers.models import Customer
from products.models import Product
from payments.models import Payment


class Sale(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(
        Customer, models.SET_NULL, db_column="customer", blank=True, null=True
    )
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax_percentage = models.FloatField(default=0)
    amount_payed = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    # if printed add a watermark to the receipt
    receipt_is_printed = models.BooleanField(default=False)
    discount = models.FloatField(default=0)

    # payments
    payment = models.ManyToManyField(
        Payment,
        related_name="sales",
        blank=True,
        db_table="SalePayments",
        db_constraint=False,
        verbose_name="Payments",
    )

    class Meta:
        db_table = "Sales"
        verbose_name_plural = "Sales"
        verbose_name = "Sale"

    def __str__(self) -> str:
        return str(self.id)

    def get_total(self) -> float:
        return self.sub_total + self.tax_amount - self.discount

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


class SaleItem(models.Model):
    sale = models.ForeignKey("Sale", models.CASCADE, db_column="sale")
    product = models.ForeignKey(Product, models.CASCADE, db_column="product")
    quantity = models.IntegerField(default=1)

    def total(self):
        return self.product.price * self.quantity

    class Meta:
        db_table = "SaleItems"
        verbose_name_plural = "SaleItems"
        verbose_name = "SaleItem"

    def __str__(self) -> str:
        return f"{self.product.name} - {self.quantity}"

    def total(self):
        return self.product.price * self.quantity
