from django.urls import path
from . import views


app_name = "suppliers"

urlpatterns = [path("", views.index, name="suppliers_index")]
