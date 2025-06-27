from django.urls import path

from .views import CompanyView, index, branches, add_branch, set_up_company

app_name = "company"
urlpatterns = [
    path("<int:id>/", CompanyView.as_view(), name="company_id"),
    path("settings/", view=index, name="settings"),
    path("branches/", view=branches, name="branches"),
    path("branches/add/", view=add_branch, name="add_branch"),
    path("setup/", set_up_company, name="setup"),
]
