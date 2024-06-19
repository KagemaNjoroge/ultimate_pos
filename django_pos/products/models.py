from django.db import models


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

    class Meta:
        # Table's name
        db_table = "Product"
        verbose_name_plural = "Products"
        verbose_name = "Product"

    def __str__(self) -> str:
        return self.name

    def to_json(self):
        item = {}
        item["id"] = self.id
        item["text"] = self.name
        item["category"] = self.category.to_json()
        item["quantity"] = 1
        item["total_product"] = 0
        item["image"] = self.image.url if self.image else None
        item["track_inventory"] = self.track_inventory
        item["product_type"] = (self.product_type,)
        item["packaging_unit"] = (self.packaging_unit,)
        item["quantity_unit"] = (self.quantity_unit,)
        item["country_of_origin"] = self.country_of_origin
        return item

    def get_product_code(self) -> str:
        return f"{self.country_of_origin}{self.product_type}{self.packaging_unit}{self.quantity_unit}"
