from django.db import models


class Company(models.Model):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(blank=True, null=True, default="static/default.png")
    company_name = models.CharField(max_length=100, blank=False, null=False)
    currency_symbol = models.CharField(max_length=5, default="Kes")
    kra_pin = models.CharField(max_length=11, blank=True, null=True)

    def __str__(self) -> str:
        return self.company_name

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "phone": self.phone_number,
            "email": self.email,
            "city": self.city,
            "address": self.address,
            "company_name": self.company_name,
            "currency": self.currency_symbol,
            # if photo
            "logo": self.logo.url or None,
            "kra_pin": self.kra_pin,
        }

    class Meta:
        verbose_name_plural = "Companies"
        verbose_name = "Company"
        db_table = "Company"


class Branch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    branch_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    branch_id = models.CharField(max_length=10, blank=True, null=True)
    is_headquarter = models.BooleanField(default=False)

    logo = models.ImageField(blank=True, null=True, default="static/default.png")

    def __str__(self) -> str:
        return self.branch_name

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "company": self.company.to_dict(),
            "branch_name": self.branch_name,
            "phone": self.phone_number,
            "email": self.email,
            "address": self.address,
            "branch_id": self.branch_id,
            "is_headquarter": self.is_headquarter,
            "logo": self.logo.url,
        }

    class Meta:
        verbose_name_plural = "Branches"
        verbose_name = "Branch"
        db_table = "Branch"


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
        return self.id

    class Meta:
        verbose_name_plural = "Subscriptions"
        verbose_name = "Subscription"
        db_table = "Subscription"

    def to_dict(self):
        return {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "is_active": self.is_active,
            "notes": self.notes,
        }
