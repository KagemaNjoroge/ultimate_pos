from django.db import models
from suppliers.models import Supplier
from utils.models import Photo


class Category(models.Model):
    STATUS_CHOICES = (("ACTIVE", "Active"), ("INACTIVE", "Inactive"))  # new

    name = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the category",
        default="ACTIVE",
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
    # a product can have multiple images
    photos = models.ManyToManyField(
        Photo,
        related_name="product_photos",
        blank=True,
        verbose_name="Product Photos",
    )
    display_image = models.ImageField(
        upload_to="products", blank=True, null=True
    )  # this is the one displayed in the product list
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

    class Meta:
        db_table = "Product"
        verbose_name_plural = "Products"
        verbose_name = "Product"

    def __str__(self) -> str:
        return self.name

    @property
    def get_sku(self):
        return f"{self.category.name[:3].upper()}-{self.id:05d}"

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "track_inventory": self.track_inventory,
            "display_image": self.display_image.url if self.display_image else None,
            "status": self.status,
            "category": self.category.name,
            "price": self.price,
            "id": self.id,
        }
