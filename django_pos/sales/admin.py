from django.contrib import admin

from .models import Sale, SaleDetail


class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_added', 'grand_total', 'customer')


class SaleDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'sale', 'product', 'quantity', 'price')


admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleDetail, SaleDetailAdmin)
