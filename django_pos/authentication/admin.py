from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    
    list_display = ("username", "role", "email", "phone_number", "date_of_birth")
    list_filter = ("role",)
    search_fields = ("username", "email", "role")
    list_per_page = 10
    ordering = ("username",)
    actions = ["activate", "deactivate"]

    @admin.action(description="Activate selected users")
    def activate(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Activated successfully")

    @admin.action(description="Deactivate selected users")
    def deactivate(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Deactivated successfully")
