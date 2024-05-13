from django.urls import path

app_name = "cloud"

from . import views


urlpatterns = [path("", views.index, name="cloud")]
