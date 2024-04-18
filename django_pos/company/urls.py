from django.urls import path

from .views import CompanyView, index

app_name = "company"
urlpatterns = [
    path("", CompanyView.as_view()),
    path("<int:id>/", CompanyView.as_view()),
    path("settings/", view=index, name="settings"),
]
