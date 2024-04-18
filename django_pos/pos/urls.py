from django.urls import path

from . import views

app_name = "pos"
urlpatterns = [
    path("", views.index, name="index"),
    path("pos/", views.pos, name="pos"),
    path("notifications/", views.get_notifications, name="notifications"),
    path("notifications/<int:id>/", views.get_notifications, name="notifications"),
    path("subscription/", view=views.subscription_page, name="subscription_page"),
    path("management/", view=views.register_company, name="resgister_company"),
]
