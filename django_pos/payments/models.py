from utils.models import TimestampedModel
from django.db import models


class Payment(TimestampedModel):
    """
    Represents a payment made by a customer.
    """

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    payment_method = models.CharField(max_length=50)
    reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("completed", "Completed"),
            ("failed", "Failed"),
            ("refunded", "Refunded"),
        ],
    )

    def __str__(self):
        return f"{self.amount} {self.currency} - {self.status}"
