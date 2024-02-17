from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, FloatField, F
from django.db.models.functions import Coalesce
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from customers.models import Customer
from products.models import Product, Category
from sales.models import Sale
from company.models import Company
import json


@login_required(login_url="/accounts/login/")
def index(request):
    today = date.today()

    year = today.year
    monthly_earnings = []

    # Calculate earnings per month
    for month in range(1, 13):
        earning = Sale.objects.filter(date_added__year=year, date_added__month=month).aggregate(
            total_variable=Coalesce(Sum(F('grand_total')), 0.0, output_field=FloatField())).get('total_variable')
        monthly_earnings.append(earning)

    # Calculate annual earnings
    annual_earnings = Sale.objects.filter(date_added__year=year).aggregate(total_variable=Coalesce(
        Sum(F('grand_total')), 0.0, output_field=FloatField())).get('total_variable')
    annual_earnings = format(annual_earnings, '.2f')

    # AVG per month
    avg_month = format(sum(monthly_earnings) / 12, '.2f')

    # Top-selling products
    top_products = Product.objects.annotate(quantity_sum=Sum(
        'saledetail__quantity')).order_by('-quantity_sum')[:3]

    top_products_names = []
    top_products_quantity = []

    for p in top_products:
        top_products_names.append(p.name)
        top_products_quantity.append(p.quantity_sum)

    context = {
        "active_icon": "dashboard",
        "products": Product.objects.all().count(),
        "categories": Category.objects.all().count(),
        "annual_earnings": annual_earnings,
        "monthly_earnings": json.dumps(monthly_earnings),
        "avg_month": avg_month,
        "top_products_names": json.dumps(top_products_names),
        "top_products_names_list": top_products_names,
        "top_products_quantity": json.dumps(top_products_quantity),
    }

    company = Company.objects.first()
    if company:
        context['currency_symbol'] = company.currency_symbol
    else:
        context['currency_symbol'] = "$"

    return render(request, "pos/index.html", context)


@login_required(login_url="/accounts/login/")
def pos(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        products = Product.objects.all()
        categories = Category.objects.all()
        customers = Customer.objects.all()
        return render(request, "pos/pos.html", {"products": products, "categories": categories, "customers": customers})
    elif request.method == 'POST':
        print(json.loads(request.body))
        return JsonResponse({"status": "success"})
