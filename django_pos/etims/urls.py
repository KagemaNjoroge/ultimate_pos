from django.urls import path

from . import views


app_name = "etims"
urlpatterns = [
    path("", views.etims, name="etims"),
    path("server-status/", views.get_etims_server_status, name="server-status"),
]
