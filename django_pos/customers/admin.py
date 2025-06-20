from django.contrib import admin

from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone")


admin.site.register(Customer, CustomerAdmin)
