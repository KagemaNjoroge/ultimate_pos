from django.urls import path
from .views import (
    register_user,
    logout_view,
    profile,
    index,
    no_permission_view,
    logout_api_view,
)

from django.contrib.auth.views import LoginView

app_name = "authentication"
urlpatterns = [
    path(
        "login/", LoginView.as_view(template_name="accounts/signin.html"), name="login"
    ),
    path("register/", register_user, name="register"),
    path("logout/", logout_view, name="logout"),
    path("logout-api/", logout_api_view, name="logout_api"),
    path("profile/", profile, name="profile"),
    path("", index, name="users_index"),
    path("no-permission/", no_permission_view, name="no_permission"),
]
