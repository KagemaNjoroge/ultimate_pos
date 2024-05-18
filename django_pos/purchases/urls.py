from django.urls import path
from .views import index

app_name = "purchases"

urlpatterns = [
    path("", index, name="index"),
]
