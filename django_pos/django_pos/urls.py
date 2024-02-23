from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from django_pos import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # Authentication: Login and Logout
    path('', include('authentication.urls')),
    # Index
    path('', include('pos.urls')),
    # Products
    path('products/', include('products.urls')),
    # Customers
    path('customers/', include('customers.urls')),
    # Sales
    path('sales/', include('sales.urls')),
    # Inventory
    path('inventory/', include('inventory.urls')),
    # etims
    path('etims/', include('etims.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
