from django.db import models

import company


# Create your models here.
class Company(models.Model):
    phone_number = models.CharField(max_length=20)  # Updated field type
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    logo = models.ImageField(blank=False, null=False)
    company_name = models.CharField(max_length=100, blank=False, null=False)
    currency_symbol = models.CharField(max_length=5, default="Kes")
    invoice_template_id = models.IntegerField(default=1)
    bill_template_id = models.IntegerField(default=1)

    def __str__(self) -> str:
        return self.company_name

    def to_dict(self) -> dict:
        return {
            "phone": self.phone_number,
            "email": self.email,
            "city": self.email,
            "address": self.address,
            "logo": self.logo.url,
            "company_name": self.company_name,
            "currency": self.currency_symbol,
            "invoice_template_id": self.invoice_template_id,
            "bill_template_id": self.bill_template_id,
            # if photo
            "logo": self.logo.url or None,
        }

    class Meta:
        verbose_name_plural = "Companies"
        verbose_name = "Company"
        db_table = "Company"


class Subscription(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    def deactivate_subscription(self):
        self.is_active = False
        self.save()

    def str(self):
        return self.company.company_name

    class Meta:
        verbose_name_plural = "Subscriptions"
        verbose_name = "Subscription"
        db_table = "Subscription"

    def to_dict(self):
        return {
            "company": self.company.to_dict(),
            "start_date": self.start_date,
            "end_date": self.end_date,
            "is_active": self.is_active,
            "notes": self.notes,
        }
