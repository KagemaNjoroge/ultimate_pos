from django.db import router
from django.urls import path
from rest_framework.routers import DefaultRouter


from . import views

router = DefaultRouter()
router.register("api", views.SaleViewSet, basename="sales_api")

app_name = "sales"
urlpatterns = [
    # List sales
    path("", views.sales_list_view, name="sales_list"),
    # Add sale
    path("add/", views.sales_add_view, name="sales_add"),
    # Details sale
    path("details/<str:sale_id>/", views.sales_details_view, name="sales_details"),
    # Sale receipt PDF
    path("pdf/<str:sale_id>/", views.receipt_pdf_view, name="sales_receipt_pdf"),
]


urlpatterns += router.urls
