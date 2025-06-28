from django.db import models
from products.models import Product
from company.models import Branch
from utils.models import TimestampedModel


class Inventory(TimestampedModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    alert_quantity = models.FloatField(default=1.0)
    branch = models.ForeignKey(
        to=Branch,
        on_delete=models.CASCADE,
        verbose_name="branch",
        blank=True,
        null=True,
    )

    # Cost tracking
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Stock management
    reserved_quantity = models.PositiveIntegerField(default=0)  # For pending orders
    available_quantity = models.PositiveIntegerField(default=0)  # quantity - reserved
    minimum_stock_level = models.PositiveIntegerField(default=0)  # Reorder point
    maximum_stock_level = models.PositiveIntegerField(null=True, blank=True)

    # Location tracking
    location = models.CharField(
        max_length=100, blank=True, null=True
    )  # Shelf/Bin location
    warehouse = models.CharField(max_length=100, blank=True, null=True)

    # Batch/Serial tracking
    batch_number = models.CharField(max_length=50, blank=True, null=True)
    serial_number = models.CharField(max_length=50, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    manufacturing_date = models.DateField(blank=True, null=True)

    # Status and flags
    is_active = models.BooleanField(default=True)
    is_damaged = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)

    # Supplier information
    supplier_sku = models.CharField(max_length=100, blank=True, null=True)

    # Notes and description
    notes = models.TextField(blank=True, null=True)

    # Last movement tracking
    last_restocked_date = models.DateTimeField(blank=True, null=True)
    last_sold_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"

    @property
    def is_low_stock(self):
        return self.available_quantity <= self.alert_quantity

    @property
    def stock_value(self):
        return self.quantity * self.cost_price

    def update_available_quantity(self):
        self.available_quantity = max(0, self.quantity - self.reserved_quantity)
        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "product": self.product.name,
            "quantity": self.quantity,
            "available_quantity": self.available_quantity,
            "reserved_quantity": self.reserved_quantity,
            "cost_price": float(self.cost_price),
            "selling_price": float(self.selling_price),
            "location": self.location,
            "batch_number": self.batch_number,
            "expiry_date": self.expiry_date,
            "is_low_stock": self.is_low_stock,
            "stock_value": float(self.stock_value),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "alert_quantity": self.alert_quantity,
            "branch": self.branch.branch_name if self.branch else None,
        }

    class Meta:
        verbose_name_plural = "Inventories"
        verbose_name = "Inventory"
        db_table = "Inventory"
        unique_together = ["product", "branch", "batch_number"]  # Prevent duplicates
