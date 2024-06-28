from django.contrib import admin
from .models import Inventory
from django.db.models import F


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "alert_quantity")

    search_fields = ("product__name", "product__description")
    list_per_page = 10
    ordering = ("product__name",)
    actions = ["increase_quantity", "decrease_quantity"]

    @admin.action(description="Increase quantity")
    def increase_quantity(self, request, queryset):
        queryset.update(quantity=F("quantity") + 1)
        self.message_user(request, "Quantity increased successfully")

    @admin.action(description="Decrease quantity")
    def decrease_quantity(self, request, queryset):
        queryset.update(quantity=F("quantity") - 1)
        self.message_user(request, "Quantity decreased successfully")
