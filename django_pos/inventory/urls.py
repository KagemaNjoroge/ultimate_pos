from django.db import router
from django.urls import path
from .views import index, add_inventory, update_inventory, InventoryViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# api routes
router.register(r"api", InventoryViewSet, basename="inventory_api")


app_name = "inventory"
urlpatterns = [
    path("", index, name="inventory_index"),
    path("add/", add_inventory, name="inventory_add"),
    path("update/<int:inventory_id>/", update_inventory, name="update_inventory"),
]


urlpatterns += router.urls
