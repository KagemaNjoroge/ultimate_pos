from django.urls import path
from rest_framework.routers import DefaultRouter


from company.views import BranchesViewSet, CompanyView
from authentication.views import (
    profile,
    no_permission_view,
    DecoratedTokenObtainPairView,
    DecoratedTokenRefreshView,
)
from customers.views import CustomerApiViewSet
from expenses.views import ExpenseCategoryViewSet, ExpenseViewSet
from products.views import CategoryApiViewSet, ProductApiViewSet, TaxGroupApiViewSet
from inventory.views import InventoryViewSet
from suppliers.views import SupplierApiViewSet
from sales.views import SaleViewSet, receipt_pdf_view
from payments.views import PaymentViewSet
from utils.views import PhotoApiViewSet
from pos.views import NotificationsView, dashboard

router = DefaultRouter()


router.register(r"branch", BranchesViewSet, basename="branch")
router.register(r"customers", CustomerApiViewSet, basename="customers")
router.register(
    r"expense-categories", ExpenseCategoryViewSet, basename="expense-category"
)
router.register(r"expenses", ExpenseViewSet, basename="expense")
router.register(r"product-categories", CategoryApiViewSet, basename="category")
router.register(r"products", ProductApiViewSet, basename="product")
router.register(r"tax-groups", TaxGroupApiViewSet, basename="tax-group")
router.register(r"inventory", InventoryViewSet, basename="inventory")
router.register(r"suppliers", SupplierApiViewSet, basename="supplier")
router.register(r"sales", SaleViewSet, basename="sales")
router.register(r"payments", PaymentViewSet, basename="payments")
router.register(r"photos", PhotoApiViewSet, basename="photos")

urlpatterns = [
    # company
    path("company/<int:id>/", CompanyView.as_view(), name="company_id"),
    path("company/", CompanyView.as_view(), name="company"),
    # authentication
    path("auth/profile/", profile, name="profile"),
    path("auth/no-permission/", no_permission_view, name="no_permission"),
    # JWT Token Authentication
    path(
        "auth/token/",
        DecoratedTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "auth/token/refresh/",
        DecoratedTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    # sales pdf receipt
    path("sales/pdf/<str:sale_id>/", receipt_pdf_view, name="sales_receipt_pdf"),
    path("notifications/", NotificationsView.as_view(), name="notifications_list"),
    path(
        "notifications/<int:id>/",
        NotificationsView.as_view(),
        name="notifications_detail",
    ),
    path("pos/dashboard/", dashboard, name="dashboard"),
]


urlpatterns += router.urls
