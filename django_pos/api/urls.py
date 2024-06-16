from rest_framework.routers import DefaultRouter

from .vie.customers import CustomersViewSet
from .vie.expenses import ExpensesViewSet, ExpenseCategoryViewSet

app_name = 'api'
router = DefaultRouter()
router.register(r"expenses", ExpensesViewSet, basename="expenses")
router.register("expense-category", ExpenseCategoryViewSet, basename="expense_category")
router.register("customers", CustomersViewSet, basename="customers")
urlpatterns = router.urls
