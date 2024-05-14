from django.urls import path
from . import views

app_name = "expenses"

urlpatterns = [
    path("<int:id>", views.index, name="expenses_operations"),
    path("", views.index, name="index"),
    path("category", views.expense_categories, name="category"),
]
