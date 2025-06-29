from django.contrib import admin
from .models import Expense, ExpenseCategory

# Register your models here.


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("expense_name", "category", "amount", "created_at", "updated_at")
    search_fields = ("expense_name", "category__category_name", "amount")
    list_filter = ("category", "created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    list_per_page = 10


class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "category_description", "is_recurring")
    search_fields = ("category_name", "category_description")
    list_filter = ("is_recurring",)
    ordering = ("category_name",)
    list_per_page = 10


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)
