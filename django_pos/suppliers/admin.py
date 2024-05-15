from django.contrib import admin
from .models import Supplier

# Register your models here.


class SupplierAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "address",
        "phone",
        "email",
        "kra_pin",
        "website",
        "logo",
        "branch",
    ]
    search_fields = [
        "name",
        "address",
        "phone",
        "email",
        "kra_pin",
        "website",
        "logo",
        "branch",
    ]
    list_filter = [
        "name",
        "address",
        "phone",
        "email",
        "kra_pin",
        "website",
        "logo",
        "branch",
    ]
    list_per_page = 10


admin.site.register(Supplier, SupplierAdmin)
