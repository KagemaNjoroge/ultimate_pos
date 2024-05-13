from django.contrib import admin
from .models import Company, Subscription, Branch


class BranchAdmin(admin.ModelAdmin):
    list_display = (
        "branch_name",
        "phone_number",
        "email",
        "city",
        "address",
        "branch_id",
    )
    # should not be able to add or change branch details

    # def has_add_permission(self, request):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_module_permission(self, request):
    #     return False


admin.site.register(Branch, BranchAdmin)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("company_name", "phone_number", "currency_symbol")
    # should not be able to add or change company details

    # def has_add_permission(self, request):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


class SubscriptionAdmin(admin.ModelAdmin):
    # should not be able to add or change subscription details
    list_display = ("company", "start_date", "end_date", "is_active")

    # comment out for testing
    # def has_add_permission(self, request):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


admin.site.register(Company, CompanyAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
