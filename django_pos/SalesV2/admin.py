from django.contrib import admin
from .models import Sale, SaleItem


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date_added",
        "customer",
        "sub_total",
        "discount",
        "grand_total",
        "total_tax_amount",
        "amount_paid",
        "amount_change",
        "receipt_is_printed",
    )
    list_filter = ("date_added", "customer", "receipt_is_printed")
    search_fields = ("id", "customer__first_name", "customer__last_name")
    ordering = ("date_added",)
    date_hierarchy = "date_added"


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity")
    list_filter = ("product",)
    search_fields = ("product__name",)
    ordering = ("product",)
