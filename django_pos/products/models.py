from django.db import models
from django.forms import model_to_dict



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
        # permissions
        permissions = [
            ("can_view_category", "Can view category"),
            ("can_add_category", "Can add category"),
            ("can_edit_category", "Can edit category"),
            ("can_delete_category", "Can delete category"),
        ]

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

    # def save(self, *args, **kwargs):
    #     # if track inventory, create a new inventory record
    #     if self.track_inventory:
    #         Inventory.objects.create(product=self, quantity=0)

    class Meta:
        # Table's name
        db_table = "Product"
        verbose_name_plural = "Products"
        verbose_name = "Product"
        # permissions
        permissions = [
            ("can_view_product", "Can view product"),
            ("can_add_product", "Can add product"),
            ("can_edit_product", "Can edit product"),
            ("can_delete_product", "Can delete product"),
        ]

    def __str__(self) -> str:
        return self.name

    def to_json(self):
        item = model_to_dict(self)
        item["id"] = self.id
        item["text"] = self.name
        item["category"] = self.category.name
        item["quantity"] = 1
        item["total_product"] = 0
        # if image exists, then return the image url, else return empty string
        item["image"] = self.image.url if self.image else ""
        item["track_inventory"] = self.track_inventory
        return item
