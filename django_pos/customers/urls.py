from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from .api import CustomerViewSet

router = DefaultRouter()
router.register(r"api", CustomerViewSet, basename="customers_api")

app_name = "customers"
urlpatterns = [
    # List customers
    path("", views.customers_list_view, name="customers_list"),
    # Add customer
    path("add", views.customers_add_view, name="customers_add"),
    # Update customer
    path(
        "update/<str:customer_id>", views.customers_update_view, name="customers_update"
    ),
    # Delete customer
    path(
        "delete/<str:customer_id>", views.customers_delete_view, name="customers_delete"
    ),
    # Customer profile
    path(
        "profile/<str:id>",
        views.customer_profile,
        name="customer_profile",
    ),
]


# api urls

# urlpatterns += router.urls
