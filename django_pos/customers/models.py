from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    address = models.TextField(max_length=256, blank=True, null=True)
    email = models.EmailField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    kra_pin = models.CharField(max_length=12, default="A000000000Z", blank=True, null=True)

    class Meta:
        db_table = 'Customers'
        verbose_name_plural = 'Customers'
        verbose_name = 'Customer'

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def to_select2(self):
        item = {
            "label": self.get_full_name(),
            "value": self.id
        }
        return item
