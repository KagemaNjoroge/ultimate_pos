from django.contrib import admin
from django.http import HttpRequest
from .models import Company, Branch


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("company_name", "phone_number", "city")

    def has_add_permission(self, request: HttpRequest) -> bool:
        return Company.objects.all().count() < 1


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):

    fields = (
        "company",
        "branch_name",
        "phone_number",
        "is_headquarter",
        "logo",
    )

    list_display = (
        "branch_name",
        "phone_number",
        "is_headquarter",
    )

