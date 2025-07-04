from .views import mpesa_daraja_callback
from django.urls import path

urlpatterns = [
    # M-Pesa Daraja API callback endpoint
    path("mpesa-daraja-callback/", mpesa_daraja_callback, name="mpesa_daraja_callback"),
]
