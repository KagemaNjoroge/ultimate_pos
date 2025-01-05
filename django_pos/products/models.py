from django.db import models
from suppliers.models import Supplier


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
        db_table = "Category"
        verbose_name_plural = "Categories"
        verbose_name = "Category"

    def __str__(self) -> str:
        return self.name

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "status": self.status,
            "description": self.description,
            "id": self.id,
        }


class Product(models.Model):
    STATUS_CHOICES = (("ACTIVE", "Active"), ("INACTIVE", "Inactive"))  # new
    PRODUCT_TYPES = (
        ("1", "Raw Material"),
        ("2", "Finished Product"),
        (
            "3",
            "Service without stock",
        ),
    )
    supplier = models.ForeignKey(
        to=Supplier,
        on_delete=models.CASCADE,
        verbose_name="supplier",
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    track_inventory = models.BooleanField(default=False)
    image = models.ImageField(upload_to="products", blank=True, null=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the product",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        related_name="category",
        on_delete=models.CASCADE,
        db_column="category",
    )
    price = models.FloatField(default=0)

    # etims related
    country_of_origin = models.CharField(max_length=5, blank=True, null=True)
    product_type = models.CharField(
        max_length=30,
        choices=PRODUCT_TYPES,
        verbose_name="Product Type",
        default="Finished Product",
    )
    packaging_unit = models.CharField(max_length=20, blank=True, null=True)
    quantity_unit = models.CharField(max_length=20, blank=True, null=True)
    barcode = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "Product"
        verbose_name_plural = "Products"
        verbose_name = "Product"

    def __str__(self) -> str:
        return self.name

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "track_inventory": self.track_inventory,
            "image": self.image.url,
            "status": self.status,
            "category": self.category.name,
            "price": self.price,
            "id": self.id,
            "country_of_origin": self.country_of_origin,
            "product_type": self.product_type,
            "packaging_unit": self.packaging_unit,
            "quantity_unit": self.quantity_unit,
            "barcode": self.barcode,
        }
