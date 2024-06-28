from django.urls import path
from . import views

app_name = "suppliers"

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.add_supllier_template, name="new"),
]
