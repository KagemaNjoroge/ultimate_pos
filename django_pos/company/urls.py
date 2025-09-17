from django.urls import path
from rest_framework.routers import DefaultRouter


app_name = "company"
from .views import (
    CompanyView,
    BranchesViewSet,
    index,
    branches,
    add_branch,
    set_up_company,
)

router = DefaultRouter()
router.register(r"branch/api", BranchesViewSet, basename="branch")


urlpatterns = [
    path("api/<int:id>/", CompanyView.as_view(), name="company_id"),
    path("api/", CompanyView.as_view(), name="company"),
    path("settings/", view=index, name="settings"),
    path("branches/", view=branches, name="branches"),
    path("branches/add/", view=add_branch, name="add_branch"),
    path("setup/", set_up_company, name="setup"),
]
urlpatterns += router.urls
