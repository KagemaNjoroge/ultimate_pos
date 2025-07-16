from utils.models import TimestampedModel
from django.db import models
from sales.models import Sale


class Payment(TimestampedModel):
    """
    Represents a payment made by a customer.
    """

    payment_methods = (
        ("cash", "Cash"),
        ("mpesa", "M-Pesa"),
        ("credit_card", "Credit Card"),  # visa & mastercard
    )
    sale = models.ForeignKey(
        Sale, on_delete=models.CASCADE, related_name="payments", blank=True, null=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    payment_method = models.CharField(max_length=20, choices=payment_methods)
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
