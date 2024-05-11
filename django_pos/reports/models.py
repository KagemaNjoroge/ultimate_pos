from django.db import models
from products.models import Product
from sales.models import Sale

# Create your models here.


class ProductSaleReport(models.Model):
    sale_date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product.name

    class Meta:
        db_table = "ProductSaleReports"
        verbose_name_plural = "Product Sale Reports"
        verbose_name = "Product Sale Report"
