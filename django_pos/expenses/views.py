import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render


from expenses.models import Expense, ExpenseCategory
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="/users/login/")
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


@login_required(login_url="/users/login/")
def expense_categories(request: HttpRequest, id=None) -> HttpResponse:
    if request.method == "GET":
        expense_categs = ExpenseCategory.objects.all()
        return render(
            request,
            "expenses/expense_category.html",
            context={"categories": expense_categs},
        )
    elif request.method == "POST":
        data = json.loads(request.body)
        category_name = data.get("category_name", None)
        category_description = data.get("category_description", None)
        is_recurring = data.get("is_recurring", None)

        if is_recurring == "1":
            is_recurring = True
        else:
            is_recurring = False
        if category_name:
            category = ExpenseCategory(
                category_name=category_name,
                category_description=category_description,
                is_recurring=is_recurring,
            )
            try:
                category.save()
                return JsonResponse(
                    {
                        "category": category.to_json(),
                        "status": "success",
                    }
                )
            except Exception as e:
                return JsonResponse(
                    {
                        "error": str(e),
                        "status": "error",
                    }
                )
        else:
            return JsonResponse(
                {
                    "error": "Invalid data",
                    "status": "error",
                }
            )

    elif request.method == "PUT":
        id = request.GET.get("id", None)
        if id:
            category = ExpenseCategory.objects.get(id=id)
            if request.body:
                data = json.loads(request.body)
                if "category_name" in data:
                    category.category_name = data["category_name"]
                if "category_description" in data:
                    category.category_description = data["category_description"]
                if "is_recurring" in data:
                    if data["is_recurring"] == "1":
                        category.is_recurring = True
                    else:
                        category.is_recurring = False

            try:
                category.save()
                return JsonResponse(
                    {
                        "category": category.to_json(),
                        "status": "success",
                    }
                )
            except Exception as e:
                return JsonResponse(
                    {
                        "error": str(e),
                        "status": "error",
                    }
                )
        else:
            return JsonResponse(
                {
                    "error": "Invalid data",
                    "status": "error",
                }
            )

    elif request.method == "DELETE":
        id = request.GET.get("id", None)
        category = get_object_or_404(ExpenseCategory, id=id)
        try:
            category.delete()
            return JsonResponse(
                {
                    "status": "success",
                }
            )
        except Exception as e:
            return JsonResponse(
                {
                    "error": str(e),
                    "status": "error",
                }
            )
