from rest_framework.routers import DefaultRouter
from .vie.etims import (
    EtimsBranchViewSet,
    EtimsNoticeViewSet,
    ItemClassCodesViewSet,
    UnitsOfQuantityViewSet,
)
from .vie.products import CategoryViewSet, ProductsViewSet
from .vie.customers import CustomersViewSet
from .vie.expenses import ExpensesViewSet, ExpenseCategoryViewSet
from .vie.company import CompanyViewSet, BranchViewSet, SubscriptionViewSet
from .vie.suppliers import SupplierViewset
from .vie.purchases import PurchaseViewset

app_name = "api"
router = DefaultRouter()
router.register(r"expenses", ExpensesViewSet, basename="expenses")
router.register("expense-category", ExpenseCategoryViewSet, basename="expense_category")
router.register("customers", CustomersViewSet, basename="customers")
router.register("etims-branch", EtimsBranchViewSet, basename="etims_branch")
router.register("etims-notice", EtimsNoticeViewSet, basename="etims_notice")
router.register("item-class-codes", ItemClassCodesViewSet, basename="item_class_codes")
router.register(
    "units-of-quantity", UnitsOfQuantityViewSet, basename="units_of_quantity"
)
router.register("products", ProductsViewSet, basename="products")
router.register("categories", CategoryViewSet, basename="categories")
router.register("company", CompanyViewSet, basename="company")
router.register("branch", BranchViewSet, basename="branch")
router.register("subscription", SubscriptionViewSet, basename="subscription")
router.register("purchases", PurchaseViewset, basename="purchases")
router.register("suppliers", SupplierViewset, basename="suppliers")

urlpatterns = router.urls
