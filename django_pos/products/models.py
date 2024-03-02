from email.mime import image
from django.db import models
from django.forms import model_to_dict
from django.utils.safestring import mark_safe


class Category(models.Model):
    STATUS_CHOICES = (("ACTIVE", "Active"), ("INACTIVE", "Inactive"))  # new

    name = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the category",
    )

    class Meta:
        # Table's name
        db_table = "Category"
        verbose_name_plural = "Categories"
        verbose_name = "Category"

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    STATUS_CHOICES = (("ACTIVE", "Active"), ("INACTIVE", "Inactive"))  # new

    name = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    track_inventory = models.BooleanField(default=False)
    image = models.ImageField(upload_to="products", blank=True, null=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the product",
    )
    category = models.ForeignKey(
        Category,
        related_name="category",
        on_delete=models.CASCADE,
        db_column="category",
    )

    price = models.FloatField(default=0)

    class Meta:
        # Table's name
        db_table = "Product"
        verbose_name_plural = "Products"
        verbose_name = "Product"

    def __str__(self) -> str:
        return self.name

    def to_json(self):
        item = model_to_dict(self)
        item["id"] = self.id
        item["text"] = self.name
        item["category"] = self.category.name
        item["quantity"] = 1
        item["total_product"] = 0
        # if image exists then return the image url, else return empty string
        item["image"] = self.image.url if self.image else ""
        item["track_inventory"] = self.track_inventory
        return item
