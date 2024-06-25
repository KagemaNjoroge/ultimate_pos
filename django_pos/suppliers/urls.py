from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("suppliers", views.SupplierViewSet, basename="suppliers")

app_name = "suppliers"

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.add_supllier_template, name="new"),
]
urlpatterns += router.urls
