from django.urls import path
from .views import index

app_name = 'inventory'
urlpatterns = [
    path('', index, name="inventory_index"),
]