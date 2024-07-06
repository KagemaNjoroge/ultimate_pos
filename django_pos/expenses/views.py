import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from .serializers import ExpenseCategorySerializer, ExpenseSerializer
from expenses.models import Expense, ExpenseCategory
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


@login_required(login_url="/users/login/")
@require_http_methods(["GET"])
def expenses(request: HttpRequest) -> HttpResponse:
    categories = ExpenseCategory.objects.all()
    expenses = Expense.objects.all()
    return render(
        request,
        "expenses/index.html",
        context={"expenses": expenses, "categories": categories},
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
    if request.method == "GET":
        return render(request, "expenses/new_category.html")
    elif request.method == "POST":
        data = json.loads(request.body)
        serializer = ExpenseCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@login_required(login_url="/users/login/")
@require_http_methods(["GET"])
def expense_categories(request: HttpRequest) -> HttpResponse:
    expense_categs = ExpenseCategory.objects.all()
    return render(
        request,
        "expenses/expense_category.html",
        context={"categories": expense_categs},
    )
