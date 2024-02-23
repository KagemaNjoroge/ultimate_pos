from django.db import models

from sales.models import Sale


class PaymentMethod(models.Model):
    payment_choices = [
        ('cash', 'Cash'),
        ('credit', 'Credit Card'),
        ('debit', 'Debit Card'),
        ('mpesa', 'M-Pesa'),
        ('cheque', 'Cheque'),
        ('other', 'Other')
    ]
    name = models.CharField(max_length=255, choices=payment_choices)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='payment_methods', blank=True, null=True)

    class Meta:
        db_table = 'PaymentMethods'
        verbose_name_plural = 'Payment Methods'
        verbose_name = 'Payment Method'

    def __str__(self) -> str:
        return self.name

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "logo": self.logo.url if self.logo else None
        }


class Payments(models.Model):
    sale = models.ForeignKey(
        Sale, models.PROTECT, db_column='sale')
    payment_method = models.ForeignKey(
        PaymentMethod, models.PROTECT, db_column='payment_method')
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Payments'
        verbose_name_plural = 'Payments'
        verbose_name = 'Payment'

    def __str__(self) -> str:
        return "Payment ID: " + str(self.id) + " Sale ID: " + str(self.sale.id) + " Amount: " + str(self.amount)

    def to_json(self) -> dict:
        return {
            "sale": self.sale.id,
            "payment_method": self.payment_method.name,
            "amount": self.amount,
            "date": self.date,
            "reference": self.reference
        }
