from django.contrib import admin
from .models import Notifications

admin.site.site_header = "Ultimate POS"
admin.site.site_title = "Ultimate POS Admin"
admin.site.index_title = "Welcome to Ultimate POS Admin"


@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ("title", "message", "date", "read", "user")
    list_filter = ("read",)
    search_fields = ("title", "message", "user__username")
    list_per_page = 10
    ordering = ("-date",)
    actions = ["mark_as_read", "mark_as_unread"]

    @admin.action(description="Mark selected notifications as read")
    def mark_as_read(self, request, queryset):
        queryset.update(read=True)
        # marked as read message
        self.message_user(request, "Marked as read successfully")

    @admin.action(description="Mark selected notifications as unread")
    def mark_as_unread(self, request, queryset):
        queryset.update(read=False)
        # marked as unread message
        self.message_user(request, "Marked as unread successfully")
