from django.urls import path
from .views import index, new_purchase, purchase_details

app_name = "purchases"

urlpatterns = [
    path("", index, name="index"),
    path("add/", new_purchase, name="add"),
    path("<int:id>/", purchase_details, name="purchase_details"),
]
