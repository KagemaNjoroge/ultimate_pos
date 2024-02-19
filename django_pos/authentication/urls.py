from django.urls import path
from .views import login_view, register_user, logout_view, profile

app_name = "authentication"
urlpatterns = [
    path('accounts/login/', login_view, name="login"),
    path('accounts/register/', register_user, name="register"),
    path('accounts/logout/', logout_view, name="logout"),
    path('accounts/profile/', profile, name='profile')
]
