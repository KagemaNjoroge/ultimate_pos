from django.urls import path
from .views import chat

app_name = "copilot"

urlpatterns = [
    path("chat/", chat, name="chat"),
]
