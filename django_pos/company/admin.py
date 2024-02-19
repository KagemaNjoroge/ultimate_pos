from django.contrib import admin
from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'phone_number', 'currency_symbol')


admin.site.register(Company, CompanyAdmin)
