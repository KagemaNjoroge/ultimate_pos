from django.urls import path
from .views import index, add_inventory, update_inventory


app_name = "inventory"
urlpatterns = [
    path("", index, name="inventory_index"),
    path("add/", add_inventory, name="inventory_add"),
    path("update/<str:inventory_id>", update_inventory, name="update_inventory"),
]
