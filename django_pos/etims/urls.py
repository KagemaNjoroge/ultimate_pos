from django.urls import path

from . import views


app_name = "etims"
urlpatterns = [
    path("", views.etims, name="etims"),
    path("branches/", views.get_etims_branches_list, name="branches"),
    path("notices/", views.get_etims_notices, name="notices"),
    path(
        "item-class-codes/", views.get_etims_items_class_codes, name="item-class-codes"
    ),
    path("items-list/", views.get_etims_items_list, name="items-list"),
    path("server-status/", views.get_etims_server_status, name="server-status"),
]
