from django.db import models
import django.utils.timezone
from customers.models import Customer
from products.models import Product


class Sale(models.Model):
    date_added = models.DateTimeField(default=django.utils.timezone.now)
    customer = models.ForeignKey(
        Customer, models.PROTECT, db_column="customer", blank=True, null=True
    )
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax_percentage = models.FloatField(default=0)
    amount_payed = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    # if printed add a watermark to the receipt
    receipt_is_printed = models.BooleanField(default=False)

    class Meta:
        db_table = "Sales"
        verbose_name_plural = "Sales"
        verbose_name = "Sale"

    def __str__(self) -> str:
        return str(self.id)

    def sum_items(self):
        details = SaleDetail.objects.filter(sale=self.id)
        if details.exists():
            return details.first().get_products_count()

    def to_json(self) -> dict:
        return {
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
    product = models.ForeignKey(Product, models.PROTECT, db_column="product")
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = "SaleItems"
        verbose_name_plural = "SaleItems"
        verbose_name = "SaleItem"

    def __str__(self) -> str:
        return f"{self.product.name} - {self.quantity}"

    def total(self):
        return self.product.price * self.quantity


class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, models.PROTECT, db_column="sale")
    items = models.ManyToManyField(SaleItem, db_column="items")

    def __str__(self) -> str:
        return f"{self.id}"

    def get_products_count(self) -> int:
        return self.items.count()

    def get_specific_product_count(self, product_id: int) -> int:
        return self.items.filter(product__id=product_id).count()

    def get_grand_total(self) -> float:
        return self.sale.grand_total

    class Meta:
        db_table = "SaleDetails"
        verbose_name_plural = "SaleDetails"
        verbose_name = "SaleDetail"

    def get_top_selling_products(self):
        return self.items.order_by("quantity")[:5]
