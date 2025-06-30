from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "phone",
        "email",
        "tax_id",
        "website",
    ]
    search_fields = [
        "name",
        "phone",
        "email",
        "tax_id",
        "website",
    ]
    list_filter = [
        "name",
        "phone",
        "email",
        "tax_id",
        "website",
    ]
    list_per_page = 10
