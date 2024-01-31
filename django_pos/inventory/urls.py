from django.urls import path
from .views import index, add_inventory

app_name = 'inventory'
urlpatterns = [
    path('', index, name="inventory_index"),
    path('add/', add_inventory, name="inventory_add")
]
