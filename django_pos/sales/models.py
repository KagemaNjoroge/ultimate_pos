from django.db import models
import django.utils.timezone
from customers.models import Customer
from products.models import Product


class Sale(models.Model):
    date_added = models.DateTimeField(default=django.utils.timezone.now)
    customer = models.ForeignKey(
        Customer, models.PROTECT, db_column='customer', blank=True, null=True)
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax_percentage = models.FloatField(default=0)
    amount_payed = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)

    class Meta:
        db_table = 'Sales'
        verbose_name_plural = 'Sales'
        verbose_name = 'Sale'

    def __str__(self) -> str:
        return "Sale ID: " + str(self.id) + " | Grand Total: " + str(self.grand_total) + " | Datetime: " + str(self.date_added)

    def sum_items(self):
        details = SaleDetail.objects.filter(sale=self.id)
        return sum([d.quantity for d in details])
    def to_json(self)->dict:
        return {
            "date_added": self.date_added,
            "customer": self.customer.get_full_name(),
            "sub_total": self.sub_total,
            "grand_total": self.grand_total,
            "tax_amount": self.tax_amount,
            "tax_percentage": self.tax_percentage,
            "amount_paid": self.amount_payed,
            "amount_change": self.amount_change
        }
        


class SaleDetail(models.Model):
    sale = models.ForeignKey(
        Sale, models.PROTECT, db_column='sale')
    product = models.ForeignKey(
        Product, models.PROTECT, db_column='product')
    price = models.FloatField()
    quantity = models.IntegerField()
    total_detail = models.FloatField()

    class Meta:
        db_table = 'SaleDetails'
        verbose_name_plural = 'Sale Details'
        verbose_name = 'Sale Detail'

    def __str__(self) -> str:
        return "Detail ID: " + str(self.id) + " Sale ID: " + str(self.sale.id) + " Quantity: " + str(self.quantity)
