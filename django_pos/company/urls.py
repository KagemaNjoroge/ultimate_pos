from django.urls import path

from .views import CompanyView, index, branches

app_name = "company"
urlpatterns = [
    path("", CompanyView.as_view(), name="company"),
    path("<int:id>/", CompanyView.as_view(), name="company_id"),
    path("settings/", view=index, name="settings"),
    path("branches/", view=branches, name="branches"),
]
