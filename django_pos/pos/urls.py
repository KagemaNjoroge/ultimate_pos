from django.urls import path

from . import views

app_name = "pos"
urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "notifications/", views.NotificationsView.as_view(), name="notifications_list"
    ),
    path(
        "notifications/<int:id>/",
        views.NotificationsView.as_view(),
        name="notifications_detail",
    ),
]
