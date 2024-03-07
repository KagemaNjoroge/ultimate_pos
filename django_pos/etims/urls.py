from django.urls import path

from . import views


app_name = "etims"
urlpatterns = [
    path("", views.etims, name="etims"),
]
