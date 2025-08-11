from django.db import models
from suppliers.models import Supplier
from utils.models import Photo, TimestampedModel


class Category(TimestampedModel):
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


class TaxGroup(TimestampedModel):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    tax_rate = models.FloatField(default=0.0)

    statuses = (("ACTIVE", "Active"), ("INACTIVE", "Inactive"))
    status = models.CharField(
        choices=statuses,
        max_length=100,
        verbose_name="Status of the tax group",
        default="ACTIVE",
    )

    class Meta:
        db_table = "TaxGroup"
        verbose_name_plural = "Tax Groups"
        verbose_name = "Tax Group"

    def __str__(self):
        return self.name


class Product(TimestampedModel):
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
    # tax group
    tax_group = models.ForeignKey(
        TaxGroup,
        related_name="tax_group",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "Product"
        verbose_name_plural = "Products"
        verbose_name = "Product"

    def __str__(self) -> str:
        return self.name

    @property
    def get_sku(self):
        return f"{self.category.name[:3].upper()}-{self.id:05d}"

    def _get_tax_rate(self):
        if self.tax_group:
            return self.tax_group.tax_rate
        else:
            return float(0)

    @property
    def tax_rate(self):
        return self._get_tax_rate()
