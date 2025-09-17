from django.db import models

from customers.models import Customer
from products.models import Product
from utils.models import TimestampedModel


class SaleItem(models.Model):

    product = models.ForeignKey(Product, models.CASCADE, db_column="product")
    quantity = models.IntegerField(default=1)

    def get_tax_percentage(self):
        if self.product.tax_group:
            return self.product.tax_group.tax_rate
        return 0

    def get_tax_amount(self):
        tax_percentage = self.get_tax_percentage()
        return (self.product.price * self.quantity * tax_percentage) / 100

    def total(self):
        return self.product.price * self.quantity + self.get_tax_amount()

    class Meta:
        db_table = "SaleItems"
        verbose_name_plural = "SaleItems"
        verbose_name = "SaleItem"

    def __str__(self) -> str:
        return f"{self.product.name} - {self.quantity}"

    def total(self):
        return self.product.price * self.quantity


class Sale(TimestampedModel):

    customer = models.ForeignKey(
        Customer, models.SET_NULL, db_column="customer", blank=True, null=True
    )
    items = models.ManyToManyField(SaleItem, blank=True)
    discount = models.FloatField(default=0)

    def _get_total_tax(self):
        total_tax = 0
        for item in self.items.all():
            total_tax += item.get_tax_amount()
        return total_tax

    def _get_sub_total(self):
        sub_total = 0
        for item in self.items.all():
            sub_total += item.total()
        return sub_total

    def _grand_total(self):
        return self._get_sub_total() - self.discount

    @property
    def sub_total(self):
        return self._get_sub_total()

    @property
    def grand_total(self):
        return self._grand_total()

    # if printed add a watermark to the receipt
    receipt_is_printed = models.BooleanField(default=False)

    class Meta:
        db_table = "Sales"
        verbose_name_plural = "Sales"
        verbose_name = "Sale"

    def __str__(self) -> str:
        return str(self.id)
