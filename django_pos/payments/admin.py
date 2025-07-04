from django.contrib import admin
from .models import ResponseData


@admin.register(ResponseData)
class ResponseDataAdmin(admin.ModelAdmin):
    """
    Admin interface for managing ResponseData model.
    """

    list_display = ("id", "created_at")
    search_fields = ("id",)
    readonly_fields = ("created_at",)

    def has_add_permission(self, request):
        """
        Disable add permission to prevent manual entry of response data.
        """
        return False
