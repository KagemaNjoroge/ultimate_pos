from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


schema_view = get_schema_view(
    openapi.Info(
        title="UltimatePOS API",
        default_version="v1",
        description="Ultimate POS API Documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="nyamburanjorogejames@students.uonbi.ac.ke"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Authentication: Login and Logout
    path("accounts/", include("authentication.urls")),
    # Index
    path("", include("pos.urls")),
    # Products
    path("products/", include("products.urls")),
    # Customers
    path("customers/", include("customers.urls")),
    # Sales
    path("sales/", include("sales.urls")),
    # Inventory
    path("inventory/", include("inventory.urls")),
    # reports
    path("reports/", include("reports.urls")),
    # company
    path("company/", include("company.urls")),
    # suppliers
    path("suppliers/", include("suppliers.urls")),
    # expenses
    path("expenses/", include("expenses.urls")),
    # Swagger
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # api authentication
    path("api-auth/", include("rest_framework.urls")),
    # Utils
    path("utils/", include("utils.urls")),
    # Payments
    path("payments/", include("payments.urls")),
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
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += debug_toolbar_urls()
