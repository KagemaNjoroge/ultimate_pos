from django.contrib import admin
from .models import Inventory


class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'date_added', 'date_modified']


admin.site.register(Inventory, InventoryAdmin)
