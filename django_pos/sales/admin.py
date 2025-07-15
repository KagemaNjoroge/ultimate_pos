from django.contrib import admin

from .models import Sale, SaleItem


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "grand_total", "customer")
    list_filter = ("created_at", "customer")
    search_fields = ("customer__first_name", "customer__last_name")


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity")
    list_filter = ("product",)
    search_fields = ("product__name",)
