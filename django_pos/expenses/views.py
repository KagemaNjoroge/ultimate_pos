from calendar import c
import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from expenses.models import Expense, ExpenseCategory

# Create your views here.


def index(request: HttpRequest) -> HttpResponse:

    if request.method == "GET":
        recent_expenses = Expense.objects.order_by("-date_added")[:10]
        all_expense_categories = ExpenseCategory.objects.all()
        return render(
            request,
            "expenses/index.html",
            {"expenses": recent_expenses, "categories": all_expense_categories},
        )
    elif request.method == "POST":
        description = request.POST.get("description", "")
        category = request.POST.get("category", None)
        amount = request.POST.get("amount", 0.00)
        name = request.POST.get("expense_name", None)

        if category and name:
            category = ExpenseCategory.objects.get(id=category)
            expense = Expense(
                expense_description=description,
                category=category,
                amount=amount,
                expense_name=name,
            )
            expense.save()
            return JsonResponse(
                {
                    "expense": expense.to_json(),
                    "status": "success",
                }
            )
        else:
            return JsonResponse({"error": "Invalid data", "status": "error"})
    elif request.method == "PUT":
        id = request.GET.get("id", None)

        if id:
            expense = Expense.objects.get(id=id)
            if request.body:
                data = json.loads(request.body)
                if "description_" in data:
                    expense.expense_description = data["description_"]
                if "category_" in data:
                    expense.category = ExpenseCategory.objects.get(id=data["category_"])
                if "amount_" in data:
                    expense.amount = data["amount_"]
                if "name" in data:
                    expense.expense_name = data["name"]

            expense.save()
            return JsonResponse(
                {
                    "expense": expense.to_json(),
                    "status": "success",
                }
            )
        else:
            return JsonResponse({"error": "Invalid data", "status": "error"})
    elif request.method == "DELETE":
        id = request.GET.get("id", None)
        if id:
            try:
                expense = Expense.objects.get(id=id)
                expense.delete()
                return JsonResponse(
                    {
                        "status": "success",
                    }
                )
            except Expense.DoesNotExist:
                return JsonResponse(
                    {
                        "error": "Expense does not exist",
                        "status": "error",
                    }
                )

        else:
            return JsonResponse({"error": "Invalid data", "status": "error"})


def expense_categories(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        expense_categs = ExpenseCategory.objects.all()
        return render(
            request,
            "expenses/expense_category.html",
            context={"categories": expense_categs},
        )
    elif request.method == "POST":
        data = request.POST
        print(data)
        return JsonResponse({"name": "UltimatePOS"})
