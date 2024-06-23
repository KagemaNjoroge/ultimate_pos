from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "status")
    list_filter = ("status",)
    search_fields = ("name", "description")
    list_per_page = 10
    ordering = ("name",)
    actions = ["activate", "deactivate"]

    @admin.action(description="Activate selected categories")
    def activate(self, request, queryset):
        queryset.update(status="ACTIVE")
        self.message_user(request, "Activated successfully")

    @admin.action(description="Deactivate selected categories")
    def deactivate(self, request, queryset):
        queryset.update(status="INACTIVE")
        self.message_user(request, "Deactivated successfully")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "track_inventory", "status", "category")
    list_filter = ("status", "track_inventory", "category")
    search_fields = ("name", "description", "category__name")
    list_per_page = 10
    ordering = ("name",)
    actions = ["activate", "deactivate"]

    @admin.action(description="Activate selected products")
    def activate(self, request, queryset):
        queryset.update(status="ACTIVE")
        self.message_user(request, "Activated successfully")

    @admin.action(description="Deactivate selected products")
    def deactivate(self, request, queryset):
        queryset.update(status="INACTIVE")
        self.message_user(request, "Deactivated successfully")
