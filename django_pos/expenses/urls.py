from django.urls import path
from .views import expense_categories, expenses, add_expense, add_expense_category

app_name = "expenses"


urlpatterns = [
    path("", expenses, name="index"),
    path("category/", expense_categories, name="category"),
    path("add/", add_expense, name="add_expense"),
    path("category/<int:id>/", expense_categories, name="category_operations"),
    path("add-category/", add_expense_category, name="add_expense_category"),
]
