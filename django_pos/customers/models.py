from django.db import models
from utils.models import TimestampedModel


class Customer(TimestampedModel):

    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    address = models.TextField(max_length=256, blank=True, null=True)
    email = models.EmailField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    tax_number = models.CharField(
        max_length=12, default="A000000000Z", blank=True, null=True
    )
    is_active = models.BooleanField(default=True)
    photo = models.FileField(
        upload_to="customers", blank=True, null=True, default="/img/undraw_profile.svg"
    )

    class Meta:
        db_table = "Customers"
        verbose_name_plural = "Customers"
        verbose_name = "Customer"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self) -> str:
        """
        Returns:
          str: The full name of the customer.
        """
        return f"{self.first_name} {self.last_name}"
