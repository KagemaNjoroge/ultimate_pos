from django.urls import path
from .views import index, duration_sales_report

app_name = "reports"
urlpatterns = [
    path("", index, name="index"),
    path("duration-sales-report/", duration_sales_report, name="duration_sales_report"),
]
