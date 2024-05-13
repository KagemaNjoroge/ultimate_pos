from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from pydantic import Json
from pos.views import check_subscription
from django.contrib.auth.decorators import login_required
from datetime import datetime
from sales.models import Sale, SaleDetail
from django.views.decorators.http import require_http_methods

# Create your views here.


@login_required(login_url="/users/login/")
@check_subscription
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "reports/index.html", context={"active_icon": "reports"})


@login_required(login_url="/users/login/")
@check_subscription
@require_http_methods(["GET"])
def duration_sales_report(request: HttpRequest):
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

    return JsonResponse(
        data=[sale.to_json() for sale in sales],
        status=200,
        safe=False,
    )


@login_required(login_url="/users/login/")
@check_subscription
@require_http_methods(["GET"])
def sales_this_month(request: HttpRequest) -> JsonResponse:
    sales = Sale.objects.filter(
        date_added__range=[
            datetime.now().replace(day=1),
            datetime.now().replace(day=31),
        ]
    )

    total = sum([sale.grand_total for sale in sales])

    return JsonResponse(
        data={
            "total": total,
            "sales": [sale.to_json() for sale in sales],
            "count": sales.count(),
        },
        status=200,
        safe=False,
    )


@login_required(login_url="/users/login/")
@check_subscription
@require_http_methods(["GET"])
def sales_this_week(request: HttpRequest) -> JsonResponse:
    sales = Sale.objects.filter(
        date_added__range=[
            datetime.now().replace(day=1),
            datetime.now().replace(day=7),
        ]
    )

    total = sum([sale.grand_total for sale in sales])

    return JsonResponse(
        data={
            "total": total,
            "sales": [sale.to_json() for sale in sales],
            "count": sales.count(),
        },
        status=200,
        safe=False,
    )


@login_required(login_url="/users/login/")
@check_subscription
@require_http_methods(["GET"])
def best_selling_product(request: HttpRequest) -> JsonResponse:
    sales = Sale.objects.filter(
        date_added__range=[
            datetime.now().replace(day=1),
            datetime.now().replace(day=31),
        ]
    )
    tops = {}
    details = SaleDetail.objects.filter(sale__in=sales)

    for t in details:
        top = t.get_top_selling_products()
        for z in top:

            if z.product.name in tops:
                tops[z.product.name] += z.quantity
            else:
                tops[z.product.name] = z.quantity
        # get the top selling product

    return JsonResponse(
        data={"top_selling": tops},
        status=200,
        safe=False,
    )


@login_required(login_url="/users/login/")
@check_subscription
@require_http_methods(["GET"])
def get_best_selling_category(request: HttpRequest) -> JsonResponse:
    sales = Sale.objects.filter(
        date_added__range=[
            datetime.now().replace(day=1),
            datetime.now().replace(day=31),
        ]
    )
    tops = {}
    details = SaleDetail.objects.filter(sale__in=sales)

    for t in details:
        top = t.get_top_selling_products()
        for z in top:

            if z.product.category in tops:
                tops[z.product.category] += z.quantity
            else:
                tops[z.product.category] = z.quantity

    return JsonResponse(
        data={"top_selling": [tp.to_json() for tp in tops]},
        status=200,
        safe=False,
    )
