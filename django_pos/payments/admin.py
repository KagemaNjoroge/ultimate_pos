from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "sale",
        "amount",
        "currency",
        "payment_method",
        "reference",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = ("sale__id", "reference", "status")
    list_filter = ("payment_method", "status", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
