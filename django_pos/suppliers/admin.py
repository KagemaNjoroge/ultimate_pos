from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "phone",
        "email",
        "kra_pin",
        "website",
        "branch",
    ]
    search_fields = [
        "name",
        "phone",
        "email",
        "kra_pin",
        "website",
        "branch",
    ]
    list_filter = [
        "name",
        "phone",
        "email",
        "kra_pin",
        "website",
        "branch",
    ]
    list_per_page = 10
