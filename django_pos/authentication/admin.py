from django.contrib import admin
from .models import CustomUser, Permission


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "created_at", "updated_at")
    search_fields = ("code", "name")
    list_per_page = 10
    ordering = ("code",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = (
        "username",
        "role",
        "email",
        "phone_number",
    )
    list_filter = ("role",)
    search_fields = ("username", "email", "role")
    list_per_page = 10
    ordering = ("username",)
    actions = ["activate", "deactivate"]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "address",
                   
                )
            },
        ),
        ("Permissions", {"fields": ("role", "branch", "permissions")}),
        ("Profile Picture", {"fields": ("profile_pic",)}),
        ("Status", {"fields": ("is_active",)}),
    )

    @admin.action(description="Activate selected users")
    def activate(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Activated successfully")

    @admin.action(description="Deactivate selected users")
    def deactivate(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Deactivated successfully")
