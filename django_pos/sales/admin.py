from django.contrib import admin

from .models import Sale, SaleDetail, SaleItem


class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "date_added", "grand_total", "customer")


class SaleDetailAdmin(admin.ModelAdmin):
    list_display = ("id",)


class SaleItemAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity")


admin.site.register(SaleItem, SaleItemAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleDetail, SaleDetailAdmin)
