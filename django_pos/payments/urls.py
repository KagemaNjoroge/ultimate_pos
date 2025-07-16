from .views import PaymentViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"api", PaymentViewSet, basename="payment")


urlpatterns = []

urlpatterns += router.urls
