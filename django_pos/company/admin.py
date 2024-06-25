from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from .models import Company, Subscription, Branch


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("company_name", "phone_number", "kra_pin", "city")

    def has_add_permission(self, request: HttpRequest) -> bool:
        return Company.objects.all().count() < 1


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):

    fields = (
        "company",
        "branch_name",
        "phone_number",
        "city",
        "is_headquarter",
        "logo",
    )

    list_display = (
        "branch_name",
        "phone_number",
        "city",
        "is_headquarter",
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("start_date", "end_date", "is_active")
    actions = ["deactivate", "activate"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return False

    @admin.action(description="Deactivate subscription")
    def deactivate(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Subscription(s) deactivated")

    @admin.action(description="Activate subscription")
    def activate(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Subscription(s) activated")
