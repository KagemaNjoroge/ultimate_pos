from django.urls import path
from . import views

app_name = "expenses"

urlpatterns = [
    path("", views.index, name="index"),
]
