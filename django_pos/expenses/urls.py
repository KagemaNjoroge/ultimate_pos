from django.urls import path
from .views import (
    expense_categories,
    expenses,
    add_expense,
    add_expense_category,
    edit_expense,
    edit_category,
)

app_name = "expenses"


urlpatterns = [
    path("", expenses, name="index"),
    path("edit/<int:id>/", edit_expense, name="edit_expense"),
    path("category/", expense_categories, name="category"),
    path("category/edit/<int:id>/", edit_category, name="edit_category"),
    path("add/", add_expense, name="add_expense"),
    path("category/<int:id>/", expense_categories, name="category_operations"),
    path("add-category/", add_expense_category, name="add_expense_category"),
]
