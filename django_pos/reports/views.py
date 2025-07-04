from django.http import HttpRequest, HttpResponse
from collections import defaultdict
from datetime import datetime, timedelta
from sales.models import SaleItem
from expenses.models import Expense
from django.contrib.auth.decorators import login_required
from sales.models import Sale
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


@login_required()
def index(request: HttpRequest) -> HttpResponse:
    # get duration query params
    start_date = request.GET.get("start_date", None)
    end_date = request.GET.get("end_date", None)

    if start_date and end_date:
        # Parse the date strings
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            # If parsing fails, default to current month
            start_date = datetime.now().replace(day=1).date()
            end_date = datetime.now().date()
    else:
        # default to the past month
        start_date = datetime.now().replace(day=1).date()
        end_date = datetime.now().date()

    # Get sales within the date range
    sales = Sale.objects.filter(
        date_added__date__range=[start_date, end_date]
    ).order_by("-date_added")

    # Group sales by date for daily summary
    daily_sales = defaultdict(
        lambda: {
            "transactions": 0,
            "gross_sales": 0,
            "discounts": 0,
            "net_sales": 0,
            "date": None,
        }
    )

    for sale in sales:
        date_key = sale.date_added.date()
        daily_sales[date_key]["transactions"] += 1
        daily_sales[date_key]["gross_sales"] += sale.sub_total
        daily_sales[date_key]["discounts"] += sale.discount
        daily_sales[date_key]["net_sales"] += sale.grand_total
        daily_sales[date_key]["date"] = date_key

    # Convert to list and sort by date (most recent first)
    daily_sales_list = sorted(
        daily_sales.values(), key=lambda x: x["date"], reverse=True
    )
    # Expenses within the date range
    expenses = Expense.objects.filter(
        created_at__date__range=[start_date, end_date]
    ).order_by("-created_at")

    return render(
        request,
        "reports/index.html",
        context={
            "sales": sales,
            "daily_sales": daily_sales_list,
            "start_date": start_date,
            "end_date": end_date,
            "expenses": expenses,
            "total_sales": sum(sale.grand_total for sale in sales),
            "total_transactions": sales.count(),
            "total_expenses": sum(expense.amount for expense in expenses),
            "total_profit": sum(sale.grand_total for sale in sales)
            - sum(expense.amount for expense in expenses),
        },
    )


@login_required()
@api_view(["GET"])
def duration_sales_report(request):
    # get duration span
    start_date = request.GET.get("start_date", None)
    end_date = request.GET.get("end_date", None)

    if start_date and end_date:
        sales = Sale.objects.filter(date_added__range=[start_date, end_date])
    else:
        # return for the past month
        sales = Sale.objects.filter(
            date_added__range=[
                datetime.now().replace(day=1),
                datetime.now().replace(day=31),
            ]
        )

    return Response(
        data=[sale.to_json() for sale in sales],
        status=200,
    )


@login_required()
@api_view(["GET"])
def sales_this_month(request) -> Response:

    sales = Sale.objects.filter(
        date_added__range=[
            datetime.now() - timedelta(days=28),
            datetime.now(),
        ]
    )

    total = sum([sale.grand_total for sale in sales])

    return Response(
        data={
            "total": total,
            "sales": [sale.to_json() for sale in sales],
            "count": sales.count(),
        },
        status=200,
    )


@login_required()
@api_view(["GET"])
def sales_this_week(request) -> Response:
    sales = Sale.objects.filter(
        date_added__range=[datetime.now() - timedelta(days=7), datetime.now()]
    )

    total = sum([sale.grand_total for sale in sales])

    return Response(
        data={
            "total": total,
            "sales": [sale.to_json() for sale in sales],
            "count": sales.count(),
        },
        status=200,
    )


@login_required()
@api_view(["GET"])
def best_selling_product(request) -> Response:
    sales = Sale.objects.filter(
        date_added__range=[
            datetime.now() - timedelta(days=28),
            datetime.now(),
        ]
    )
    if not sales:
        return Response(
            data={"top_selling": "No sales made"},
            status=200,
        )

    tops = {}
    sale_items = SaleItem.objects.filter(sale__in=sales)
    # count sale_item.product
    if not sale_items:
        # 404
        return Response(
            data={"top_selling": "No sales made"},
            status=404,
        )
    for item in sale_items:
        if item.product.name in tops:
            tops[item.product.name] += item.quantity
        else:
            tops[item.product.name] = item.quantity

    tops = sorted(tops.items(), key=lambda x: x[1], reverse=True)[0]

    return Response(
        data={"top_selling": tops},
        status=200,
    )


@login_required()
@api_view(["GET"])
def get_best_selling_category(request) -> Response:

    sales = Sale.objects.filter(
        date_added__range=[
            datetime.now().replace(day=1),
            datetime.now().replace(day=30),
        ]
    )

    sale_items = SaleItem.objects.filter(sale__in=sales)
    if not sale_items:
        # 404
        return Response(
            data={"top_selling": "No sales made"},
            status=404,
        )

    else:
        tops = {}
        for item in sale_items:
            if item.product.category.name in tops:
                tops[item.product.category.name] += item.quantity
            else:
                tops[item.product.category.name] = item.quantity
        tops = sorted(tops.items(), key=lambda x: x[1], reverse=True)[0]
        return Response(
            data={"top_selling": tops},
            status=200,
        )
