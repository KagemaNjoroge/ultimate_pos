from django.contrib import admin
from .models import (
    Country,
    EtimsNotice,
    TaxType,
    UnitOfQuantity,
    PackagingUnits,
    EtimsBranch,
    ItemClassCodes,
)


@admin.register(ItemClassCodes)
class ItemClassCodesAdmin(admin.ModelAdmin):
    list_display = ("itemClassCode", "itemClassCodeName")
    search_fields = ("itemClassCode", "itemClassCodeName")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("countryId", "countryCode", "countryName", "currencyCode")
    search_fields = ("countryName", "countryCode", "currencyCode")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(EtimsNotice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("noticeNumber", "title", "read")
    search_fields = ("title", "content")
    actions = ["mark_as_read"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.action(description="Mark as read")
    def mark_as_read(self, request, queryset):
        queryset.update(read=True)


@admin.register(TaxType)
class TaxTypeAdmin(admin.ModelAdmin):
    list_display = ("taxTypeName",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(UnitOfQuantity)
class UnitOfQuantityAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_display = (
        "unitOfQuantityId",
        "unitOfQuantityName",
        "unitOfQuantityDescription",
    )


@admin.register(PackagingUnits)
class PackagingUnitsAdmin(admin.ModelAdmin):
    list_display = ("packagingUnitId", "packagingUnitName", "packagingUnitDescription")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(EtimsBranch)
class EtimsBranchAdmin(admin.ModelAdmin):
    list_display = (
        "branch_tin",
        "branch_id",
        "branch_name",
        "branch_status_code",
        "province_name",
        "district_name",
        "sctr_name",
        "location_description",
        "manager_name",
        "manager_telephone",
        "manager_email",
    )
    search_fields = (
        "branch_tin",
        "branch_id",
        "branch_name",
        "province_name",
        "district_name",
        "sctr_name",
        "manager_name",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
