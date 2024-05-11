from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from pos.views import check_subscription
from django.contrib.auth.decorators import login_required
from products.models import Product
from sales.models import Sale
from django.views.decorators.http import require_http_methods

# Create your views here.


@login_required(login_url="/accounts/login/")
@check_subscription
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "reports/index.html", context={"active_icon": "reports"})


@login_required(login_url="/accounts/login/")
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
        sales = Sale.objects.filter(date_added__month=1)
    return JsonResponse(
        data=[sale.to_json() for sale in sales],
        status=200,
        safe=False,
    )
