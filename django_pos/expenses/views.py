from django.http import HttpRequest, HttpResponse
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404, render
from .serializers import ExpenseCategorySerializer, ExpenseSerializer
from expenses.models import Expense, ExpenseCategory
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Avg, Count
from django.utils import timezone
from datetime import timedelta


class ExpenseCategoryViewSet(ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer


class ExpenseViewSet(ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


@login_required(login_url="/users/login/")
@require_http_methods(["GET"])
def expenses(request: HttpRequest) -> HttpResponse:

    categories = ExpenseCategory.objects.all()
    expenses = Expense.objects.all().order_by("-created_at")

    # Calculate statistics
    total_expenses = expenses.aggregate(
        total=Sum("amount"), count=Count("id"), average=Avg("amount")
    )

    # Calculate this month's expenses
    current_month = timezone.now().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    this_month_expenses = expenses.filter(created_at__gte=current_month).aggregate(
        total=Sum("amount")
    )

    # Get recent expenses (last 7 days)
    last_week = timezone.now() - timedelta(days=7)
    recent_expenses = expenses.filter(created_at__gte=last_week)

    context = {
        "expenses": expenses,
        "categories": categories,
        "stats": {
            "total_amount": total_expenses["total"] or 0,
            "total_count": total_expenses["count"] or 0,
            "average_amount": total_expenses["average"] or 0,
            "this_month_total": this_month_expenses["total"] or 0,
            "categories_count": categories.count(),
            "recent_count": recent_expenses.count(),
        },
    }

    return render(
        request,
        "expenses/expenses.html",
        context=context,
    )


@login_required(login_url="/users/login/")
@require_http_methods(["GET"])
def add_expense(request: HttpRequest) -> HttpResponse:
    categories = ExpenseCategory.objects.all()
    return render(
        request,
        "expenses/new_expense.html",
        context={"categories": categories},
    )


@login_required(login_url="/users/login/")
@require_http_methods(["GET"])
def add_expense_category(request: HttpRequest) -> HttpResponse:

    return render(request, "expenses/new_category.html")


@login_required(login_url="/users/login/")
@require_http_methods(["GET"])
def expense_categories(request: HttpRequest) -> HttpResponse:
    expense_categs = ExpenseCategory.objects.all()
    return render(
        request,
        "expenses/expense_category.html",
        context={"categories": expense_categs},
    )


@login_required(login_url="/users/login/")
@require_http_methods(["GET"])
def edit_expense(request: HttpRequest, id: int) -> HttpResponse:
    expense = get_object_or_404(Expense, pk=id)
    categories = ExpenseCategory.objects.all()
    return render(
        request,
        "expenses/edit_expense.html",
        context={"expense": expense, "categories": categories},
    )


@login_required(login_url="/users/login/")
@require_http_methods(["GET"])
def edit_category(request: HttpRequest, id: int) -> HttpResponse:
    category = get_object_or_404(ExpenseCategory, pk=id)
    return render(
        request,
        "expenses/edit_category.html",
        context={"category": category},
    )
