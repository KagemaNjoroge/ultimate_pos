from django.urls import path
from .views import list_models, chat


urlpatterns = [
    path("models/", list_models),
    path("chat/", chat),
]
