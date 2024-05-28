from django.contrib import admin
from .models import Country, Notice, TaxType, UnitOfQuantity, PackagingUnits


# Register your models here.


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("countryId", "countryCode", "countryName", "currencyCode")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("noticeNumber", "title", "read")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TaxType)
class TaxTypeAdmin(admin.ModelAdmin):
    list_display = ("taxTypeName", "taxTypeIdentifier")

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
