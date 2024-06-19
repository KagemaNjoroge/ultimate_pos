from django.db import router
from django.urls import path
from .views import expense_categories, ExpenseView


app_name = "expenses"


urlpatterns = [
    # expenses
    path("", ExpenseView.as_view(), name="index"),
    path("<int:pk>", ExpenseView.as_view(), name="expense_operations"),
    # expense categories
    path("category", expense_categories, name="category"),
    path("category/<int:id>", expense_categories, name="category_operations"),
]
