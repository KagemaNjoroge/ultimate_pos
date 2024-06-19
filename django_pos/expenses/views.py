import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from .serializers import ExpenseCategorySerializer, ExpenseSerializer
from expenses.models import Expense, ExpenseCategory
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.parsers import JSONParser


class ExpenseView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    renderer_classes = [
        TemplateHTMLRenderer,
        JSONRenderer,
    ]
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        if request.accepted_renderer.format == "html":
            categories = ExpenseCategory.objects.all()
            return render(
                request,
                "expenses/index.html",
                context={"expenses": self.get_queryset(), "categories": categories},
            )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.accepted_renderer.format == "html":
            data = request.data
            serializer = ExpenseSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return render(
                    request,
                    "expenses/index.html",
                    context={"expenses": self.get_queryset()},
                )
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Invalid data",
                    "errors": serializer.errors,
                },
                status=400,
            )
        return super().post(request, *args, **kwargs)


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
        serializer = ExpenseCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Category added",
                    "category": serializer.data,
                }
            )
        return JsonResponse(
            {
                "status": "error",
                "message": "Invalid data",
                "errors": serializer.errors,
            },
            status=400,
        )

    elif request.method == "PUT":
        id = request.GET.get("id", None)
        if id:
            category = ExpenseCategory.objects.get(id=id)
            if request.body:
                data = json.loads(request.body)
                serializer = ExpenseCategorySerializer(
                    category, data=data, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(
                        {
                            "status": "success",
                            "message": "Category updated",
                            "category": serializer.data,
                        }
                    )
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Invalid data",
                        "errors": serializer.errors,
                    },
                    status=400,
                )
            return JsonResponse(
                {
                    "error": "Invalid data",
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
