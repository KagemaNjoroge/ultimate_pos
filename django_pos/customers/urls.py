from django.db import router
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"api", views.CustomerApiViewSet, basename="customers")

app_name = "customers"
urlpatterns = [
    # List customers
    path("", views.customers_list_view, name="customers_list"),
    # Add customer
    path("add/", views.customers_add_view, name="customers_add"),
    # Update customer
    path(
        "update/<str:customer_id>/",
        views.customers_update_view,
        name="customers_update",
    ),

    # Customer profile
    path("profile/<str:id>/", views.customer_profile, name="customer_profile"),
    # import customers
    path("import/", views.import_customers, name="import_customers"),
]


urlpatterns += router.urls
