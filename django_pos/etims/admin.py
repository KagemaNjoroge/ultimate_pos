from django.contrib import admin
from .models import Country, Notice, TaxType, UnitOfQuantity, PackagingUnits


# Register your models here.


class CountryAdmin(admin.ModelAdmin):
    list_display = ("countryId", "countryCode", "countryName", "currencyCode")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Country, CountryAdmin)


class NoticeAdmin(admin.ModelAdmin):
    list_display = ("noticeNumber", "title", "read")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Notice, NoticeAdmin)


class TaxTypeAdmin(admin.ModelAdmin):
    list_display = ("taxTypeName", "taxTypeIdentifier")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(TaxType, TaxTypeAdmin)


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


admin.site.register(UnitOfQuantity, UnitOfQuantityAdmin)


class PackagingUnitsAdmin(admin.ModelAdmin):
    list_display = ("packagingUnitId", "packagingUnitName", "packagingUnitDescription")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(PackagingUnits, PackagingUnitsAdmin)
