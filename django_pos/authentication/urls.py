from django.urls import path
from .views import (
    profile,
    no_permission_view,
    DecoratedTokenObtainPairView,
    DecoratedTokenRefreshView,
)


app_name = "authentication"
urlpatterns = [
    path("profile/", profile, name="profile"),
    path("no-permission/", no_permission_view, name="no_permission"),
    # JWT Token Authentication
    path(
        "api/token/",
        DecoratedTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        DecoratedTokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
