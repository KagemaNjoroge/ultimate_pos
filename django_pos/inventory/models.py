from django.db import models
from products.models import Product
from company.models import Branch


class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_added = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    alert_quantity = models.FloatField(default=1.0)
    branch = models.ForeignKey(
        to=Branch,
        on_delete=models.CASCADE,
        verbose_name="branch",
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.id)

    def to_dict(self):
        return {
            "id": self.id,
            "product": self.product.name,
            "quantity": self.quantity,
            "date_added": self.date_added,
            "date_modified": self.date_modified,
            "alert_quantity": self.alert_quantity,
            "branch": self.branch,
        }

    class Meta:
        verbose_name_plural = "Inventories"
        verbose_name = "Inventory"
        db_table = "Inventory"
