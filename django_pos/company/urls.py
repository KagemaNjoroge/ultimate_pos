from django.urls import path

from .views import CompanyView, index, test_firebase

app_name = "company"
urlpatterns = [
    path("", CompanyView.as_view(), name="company"),
    path("<int:id>/", CompanyView.as_view(), name="company_id"),
    path("settings/", view=index, name="settings"),
    path("test/", view=test_firebase, name="test"),
]
