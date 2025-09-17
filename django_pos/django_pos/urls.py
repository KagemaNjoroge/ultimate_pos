from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
    openapi.Info(
        title="UltimatePOS API",
        default_version="v1",
        description="Ultimate POS API Documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="nyamburanjorogejames@students.uonbi.ac.ke"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # swagger docs
    path(
        "api/docs/",
        schema_view.with_ui("swagger"),
    ),
    # api authentication
    path("api-auth/", include("rest_framework.urls")),
    # centralized router
    path("api/", include("django_pos.router")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
