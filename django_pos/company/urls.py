from django.urls import path

from .views import CompanyView, index, branches, invoice_design, add_branch

app_name = "company"
urlpatterns = [
    path("", CompanyView.as_view(), name="company"),
    path("<int:id>/", CompanyView.as_view(), name="company_id"),
    path("settings/", view=index, name="settings"),
    path("branches/", view=branches, name="branches"),
    path("branches/add/", view=add_branch, name="add_branch"),
    path("invoice-design/", view=invoice_design, name="invoice_design"),
]
