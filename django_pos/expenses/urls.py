from django.db import router
from django.urls import path
from .views import (
    expense_categories,
    expenses,
    add_expense,
    add_expense_category,
    edit_expense,
    edit_category,
    ExpenseCategoryViewSet,
    ExpenseViewSet,
)
from rest_framework.routers import DefaultRouter


app_name = "expenses"


router = DefaultRouter()

router.register(
    "api/expense-categories", ExpenseCategoryViewSet, basename="expense-category"
)
router.register("api/expenses", ExpenseViewSet, basename="expense")

urlpatterns = [
    path("", expenses, name="index"),
    path("edit/<int:id>/", edit_expense, name="edit_expense"),
    path("categories/", expense_categories, name="category"),
    path("category/edit/<int:id>/", edit_category, name="edit_category"),
    path("add/", add_expense, name="add_expense"),
    path("category/<int:id>/", expense_categories, name="category_operations"),
    path("add-category/", add_expense_category, name="add_expense_category"),
]

urlpatterns += router.urls
