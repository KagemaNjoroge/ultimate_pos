import datetime
import json
from datetime import date, datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, FloatField, F
from django.db.models.functions import Coalesce
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from company.models import Company, Subscription
from customers.models import Customer
from inventory.models import Inventory
from pos.models import Notifications
from products.models import Product, Category
from sales.models import Sale
from sales.models import SaleDetail, SaleItem


@api_view(["GET"])
def fetch_packages(request) -> Response:
    packages = [
        # hard coded packages
        {
            "id": 1,
            "name": "Starter",
            "amount": 1000,
        },
        {
            "id": 2,
            "name": "Standard",
            "amount": 2000,
        },
        {
            "id": 3,
            "name": "Premium",
            "amount": 3000,
        },
    ]
    return Response(packages)


def check_subscription(view_func):
    """
    Special decorator for making sure that the company has a subscription
    It is called before the view function
    """

    def _wrapped_view(request, *args, **kwargs):
        company = Company.objects.first()
        if not company:
            return redirect(
                "company:settings"
            )  # Redirect to a page where a company can be registered

        subscription = Subscription.objects.filter(
            company=company, is_active=True
        ).first()
        if not subscription or subscription.end_date.date() < datetime.today().date():
            return redirect("pos:subscription_page")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


@login_required(login_url="/users/login/")
def register_company(request: HttpRequest) -> HttpResponse:
    return render(
        request, "pos/register_company.html", context={"active_icon": "settings"}
    )


def subscription_page(request: HttpRequest) -> HttpResponse:
    return render(request, "pos/subscription.html", context={"active_icon": "settings"})


@login_required(login_url="/users/login/")
def index(request: HttpRequest) -> HttpResponse:
    today = date.today()

    year = today.year
    monthly_earnings = []

    # Calculate earnings per month
    for month in range(1, 13):
        earning = (
            Sale.objects.filter(date_added__year=year, date_added__month=month)
            .aggregate(
                total_variable=Coalesce(
                    Sum(F("grand_total")), 0.0, output_field=FloatField()
                )
            )
            .get("total_variable")
        )
        monthly_earnings.append(earning)

    # Calculate annual earnings
    annual_earnings = (
        Sale.objects.filter(date_added__year=year)
        .aggregate(
            total_variable=Coalesce(
                Sum(F("grand_total")), 0.0, output_field=FloatField()
            )
        )
        .get("total_variable")
    )
    annual_earnings = format(annual_earnings, ".2f")

    # AVG per month
    avg_month = format(sum(monthly_earnings) / 12, ".2f")

    f = SaleDetail.objects.all()

    # Get top products
    products = Product.objects.all()
    top = [{product.id: 0 for product in products}]

    for sale_detail in f:
        for item in sale_detail.items.all():
            for x in top:
                if item.product.id in x:
                    x[item.product.id] += item.quantity
                else:
                    x[item.product.id] = item.quantity
    x = []
    for i in top:
        for v, j in i.items():
            if j > 0:
                x.append({"id": v, "quantity": j})

    x = sorted(x, key=lambda t: t["quantity"], reverse=True)
    top_products = x[:3]

    top_products_names = []
    top_products_quantity = []

    for product in top_products:
        top_products_names.append(Product.objects.get(id=product["id"]).name)
        top_products_quantity.append(product["quantity"])

    context = {
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
        context["currency_symbol"] = company.currency_symbol
    else:
        context["currency_symbol"] = "Kshs"

    return render(request, "pos/index.html", context)


@check_subscription
@login_required(login_url="/users/login/")
def pos(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        products = Product.objects.all()
        categories = Category.objects.all()
        customers = Customer.objects.all()
        return render(
            request,
            "pos/pos.html",
            {"products": products, "categories": categories, "customers": customers},
        )
    elif request.method == "POST":
        try:
            sale_data = json.loads(request.body)
            items = sale_data["items"]
            customer_id = sale_data["customer"]
            grand_total = float(sale_data["grand_total"])
            amount_paid = float(sale_data["amount_paid"])

            change = amount_paid - grand_total
            if change < 0:
                return JsonResponse(
                    {
                        "status": "error",
                        "error_message": "Amount paid is less than total",
                    }
                )
            customer = get_object_or_404(Customer, id=customer_id)
            # hard coded tax percentage TODO: make it dynamic as per a particular product
            tax_percentage = 16
            tax_amount = grand_total * tax_percentage / 100
            sale = Sale.objects.create(
                customer=customer,
                grand_total=grand_total,
                amount_payed=amount_paid,
                amount_change=change,
                tax_percentage=tax_percentage,
                tax_amount=tax_amount,
                sub_total=grand_total - tax_amount,
            )
            sale.save()
            sale_items = []
            for item in items:
                product = get_object_or_404(Product, id=item["id"])
                attr = {
                    "product": product,
                    "price": product.price,
                    "quantity": item["count"],
                    "total_detail": product.price * item["count"],
                    "sale": sale,
                }

                # update inventory
                if product.track_inventory:
                    # check if it exists in inventory
                    inventory = Inventory.objects.filter(product=product)
                    if inventory.exists():
                        inventory = inventory.first()
                        try:
                            inventory.quantity -= int(attr["quantity"])
                            inventory.save()
                        # CHECK constraint failed: quantity must be greater than or equal to 0
                        # Check constraint errors
                        except Exception as e:
                            # add notification
                            Notifications.objects.create(
                                title="Inventory Update Failed",
                                message=f"Inventory update failed for {product.name}. \
                                    Items left: {Inventory.objects.filter(product=product).first().quantity}.",
                                user=request.user,
                            )
                            return JsonResponse(
                                {
                                    "status": "error",
                                    "error_message": f"Stock is not enough for {product.name}. \
                                    Items left: {Inventory.objects.filter(product=product).first().quantity}. \
                                        Update the inventory and try again.",
                                }
                            )
                    else:
                        pass
                # create sale items
                sale_item = SaleItem.objects.create(
                    product=product, quantity=attr["quantity"]
                )
                sale_item.save()
                sale_items.append(sale_item)
            sale_detail = SaleDetail.objects.create(sale=sale)
            sale_detail.save()
            sale_detail.items.set(sale_items)

            return JsonResponse({"status": "success", "sale_id": sale.id})
        except Exception as e:

            return JsonResponse({"status": "error", "error_message": str(e)})
    return HttpResponse("Invalid request", status=400)


@api_view(["GET"])
def get_notifications(request, id: int = None) -> Response:
    if id is None:
        notifications = Notifications.objects.filter(
            read=False, user=request.user
        ).order_by("date")
        return Response(
            [
                {
                    "id": notification.id,
                    "title": notification.title,
                    "message": notification.message,
                    "date": notification.date.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for notification in notifications
            ],
            status=200,
        )

    else:
        notification = get_object_or_404(Notifications, id=id)
        notification.read = True
        notification.save()
        return Response(
            {
                "id": notification.id,
                "title": notification.title,
                "message": notification.message,
                "date": notification.date.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )


def checkout(request: HttpRequest, amount) -> HttpResponse:
    return render(request, "pos/checkout.html", context={"amount": amount})
