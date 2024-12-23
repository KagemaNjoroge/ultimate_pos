from rest_framework.routers import DefaultRouter

from .vie.products import CategoryViewSet, ProductsViewSet
from .vie.customers import CustomersViewSet
from .vie.expenses import ExpensesViewSet, ExpenseCategoryViewSet
from .vie.company import CompanyViewSet, BranchViewSet, SubscriptionViewSet
from .vie.suppliers import SupplierViewset
from .vie.purchases import PurchaseViewset
from .vie.notifications import NotificationsViewset

app_name = "api"
router = DefaultRouter()
router.register("expenses", ExpensesViewSet, basename="expenses")
router.register("expense-category", ExpenseCategoryViewSet, basename="expense_category")
router.register("customers", CustomersViewSet, basename="customers")
router.register("products", ProductsViewSet, basename="products")
router.register("categories", CategoryViewSet, basename="categories")
router.register("company", CompanyViewSet, basename="company")
router.register("branch", BranchViewSet, basename="branch")
router.register("subscription", SubscriptionViewSet, basename="subscription")
router.register("purchases", PurchaseViewset, basename="purchases")
router.register("suppliers", SupplierViewset, basename="suppliers")
router.register("notifications", NotificationsViewset, basename="notifications")

urlpatterns = router.urls
