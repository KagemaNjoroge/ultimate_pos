from django.db import models

from customers.models import Customer
from products.models import Product
from utils.models import TimestampedModel


class Sale(TimestampedModel):

    customer = models.ForeignKey(
        Customer, models.SET_NULL, db_column="customer", blank=True, null=True
    )
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax_percentage = models.FloatField(default=0)

    # if printed add a watermark to the receipt
    receipt_is_printed = models.BooleanField(default=False)
    discount = models.FloatField(default=0)

    @property
    def amount_payed(self):
        return self.get_amount_paid()

    @property
    def amount_change(self):
        return self.get_amount_change()

    # the following methods and properties are for maintaining backward compatibility
    def get_amount_change(self):
        total_paid = self.get_amount_paid()
        return max(0, float(total_paid) - float(self.grand_total))

    def get_amount_paid(self):
        """Calculate total amount paid from all completed payments."""
        return sum(
            payment.amount for payment in self.payments.filter(status="completed")
        )

    def get_amount_due(self):
        """Calculate the amount due based on grand total and amount paid."""
        return max(0, self.grand_total - self.get_amount_paid())

    class Meta:
        db_table = "Sales"
        verbose_name_plural = "Sales"
        verbose_name = "Sale"

    def __str__(self) -> str:
        return str(self.id)

    def get_total(self) -> float:
        return self.sub_total + self.tax_amount - self.discount


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
