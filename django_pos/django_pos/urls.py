from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from debug_toolbar.toolbar import debug_toolbar_urls
from django_pos import settings

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
    # accounting
    path("accounting/", include("accounting.urls")),
    # expenses
    path("expenses/", include("expenses.urls")),
    # purchases
    path("purchases/", include("purchases.urls")),
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
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += debug_toolbar_urls()
