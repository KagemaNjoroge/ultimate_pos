from django.db import router
from django.urls import path
from .views import expense_categories, expenses

app_name = "expenses"


urlpatterns = [
    path("", expenses, name="index"),
    path("category/", expense_categories, name="category"),
    path("category/<int:id>/", expense_categories, name="category_operations"),
]
