from django.db import models
from products.models import Product


# Create your models here.


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    date_added = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.product} - {self.quantity}"

    def update_stock(self, quantity):
        self.quantity += quantity
        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "product": self.product.name,
            "quantity": self.quantity,
            "date_added": self.date_added,
            "date_modified": self.date_modified
        }

    class Meta:
        verbose_name_plural = 'Inventories'
        verbose_name = 'Inventory'
