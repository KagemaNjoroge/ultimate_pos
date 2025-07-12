from django.urls import path

from . import views

app_name = "pos"
urlpatterns = [
    path("", views.index, name="index"),
    path("pos/", views.pos, name="pos"),
    path(
        "notifications/", views.NotificationsView.as_view(), name="notifications_list"
    ),
    path(
        "notifications/<int:id>/",
        views.NotificationsView.as_view(),
        name="notifications_detail",
    ),
]
