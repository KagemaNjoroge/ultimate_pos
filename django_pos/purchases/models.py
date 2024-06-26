from django.db import models
from company.models import Branch
from products.models import Product
from suppliers.models import Supplier


class Purchase(models.Model):
    purchase_status = (
        ("PENDING", "Pending"),
        ("DONE", "Done"),
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(
        choices=purchase_status, max_length=30, verbose_name="Status of the purchase"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    branch = models.ForeignKey(
        to=Branch, blank=True, null=True, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        db_table = "Purchases"
        verbose_name_plural = "Purchases"
        verbose_name = "Purchase"
