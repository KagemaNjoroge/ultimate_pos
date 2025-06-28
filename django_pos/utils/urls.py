from django.db import router
from rest_framework.routers import DefaultRouter
from .views import PhotoApiViewSet

app_name = "utils"
router = DefaultRouter()
router.register(
    r"photos",
    PhotoApiViewSet,
    basename="photos",
)

urlpatterns = router.urls
