from django.contrib import admin
from .models import Country, Notice, TaxType, UnitOfQuantity, PackagingUnits


# Register your models here.

class CountryAdmin(admin.ModelAdmin):
    list_display = ('countryId', 'countryCode', 'countryName', 'currencyCode')


admin.site.register(Country, CountryAdmin)


class NoticeAdmin(admin.ModelAdmin):
    list_display = ('noticeNumber', 'title', 'read')


admin.site.register(Notice, NoticeAdmin)


class TaxTypeAdmin(admin.ModelAdmin):
    list_display = ('taxTypeName', 'taxTypeIdentifier')


admin.site.register(TaxType, TaxTypeAdmin)


class UnitOfQuantityAdmin(admin.ModelAdmin):
    list_display = ('unitOfQuantityId', 'unitOfQuantityName', 'unitOfQuantityDescription')


admin.site.register(UnitOfQuantity, UnitOfQuantityAdmin)


class PackagingUnitsAdmin(admin.ModelAdmin):
    list_display = ('packagingUnitId', 'packagingUnitName', 'packagingUnitDescription')


admin.site.register(PackagingUnits, PackagingUnitsAdmin)
