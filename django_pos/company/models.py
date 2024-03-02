from django.db import models


# Create your models here.
class Company(models.Model):
    phone_number = models.CharField(max_length=20)  # Updated field type
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    logo = models.ImageField(blank=False, null=False)
    company_name = models.CharField(max_length=100, blank=False, null=False)
    currency_symbol = models.CharField(max_length=5, default='Kes')
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
            "bill_template_id": self.bill_template_id
        }

    class Meta:
        verbose_name_plural = 'Companies'
        verbose_name = 'Company'
        db_table = 'Company'
