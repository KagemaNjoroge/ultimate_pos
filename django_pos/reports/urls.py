from django.urls import path
from .views import (
    index,
    duration_sales_report,
    sales_this_month,
    sales_this_week,
    best_selling_product,
    get_best_selling_category,
)

app_name = "reports"
urlpatterns = [
    path("", index, name="index"),
    path("duration-sales-report/", duration_sales_report, name="duration_sales_report"),
    path("sales-this-month/", sales_this_month, name="sales_this_month"),
    path("sales-this-week/", sales_this_week, name="sales_this_week"),
    path("best-selling-product/", best_selling_product, name="best_selling_product"),
    path(
        "best-selling-category/",
        get_best_selling_category,
        name="best_selling_category",
    ),
]
