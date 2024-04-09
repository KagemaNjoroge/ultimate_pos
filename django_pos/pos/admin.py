from django.contrib import admin
from .models import Notifications


class NotificationsAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "read", "user")
    list_filter = ("date", "read")
    search_fields = ("title", "message", "user__username")


admin.site.register(Notifications, NotificationsAdmin)
admin.site.site_header = "Ultimate POS"
admin.site.site_title = "Ultimate POS Admin"
