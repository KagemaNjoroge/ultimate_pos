from django.db import models

# Create your models here.
class Company(models.Model):
    phone_number = models.CharField(max_length=20)  # Updated field type
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    logo=models.ImageField(blank=False, null=False)
    company_name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self) -> str:
        return self.company_name