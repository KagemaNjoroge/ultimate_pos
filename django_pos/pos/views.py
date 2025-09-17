import json
from datetime import date
from django.db.models import Sum, FloatField, F
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


from .serializers import NotificationsSerializer
from customers.models import Customer
from inventory.models import Inventory
from pos.models import Notifications
from products.models import Product, Category
from sales.models import SaleItem, Sale
from rest_framework.views import APIView
from rest_framework.decorators import api_view


@api_view(["GET"])
def dashboard(request) -> Response:
    """
    Dashboard view to get various statistics.
    """
    today = date.today()

    year = today.year
    monthly_earnings = []

    # Calculate earnings per month
    for month in range(1, 13):
        earning = (
            Sale.objects.filter(created_at__year=year, created_at__month=month)
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
        Sale.objects.filter(created_at__year=year)
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

    # Get today's sales
    today_sales = (
        Sale.objects.filter(created_at__date=today)
        .aggregate(
            total_variable=Coalesce(
                Sum(F("grand_total")), 0.0, output_field=FloatField()
            )
        )
        .get("total_variable")
    )
    today_sales = format(today_sales, ".2f")

    # Get low stock items
    low_stock_items = Inventory.objects.filter(
        quantity__lte=F("alert_quantity")
    ).count()

    # Get total customers
    total_customers = Customer.objects.count()

    f = SaleItem.objects.all()

    # Get top products
    products = Product.objects.all()
    top = [{product.id: 0 for product in products}]

    for saleitem in f:
        item = saleitem
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

    top_prods = {}

    for product in top_products:
        top_prods[product["id"]] = {
            "name": Product.objects.get(id=product["id"]).name,
            "quantity": product["quantity"],
        }

    context = {
        "products": Product.objects.all().count(),
        "categories": Category.objects.all().count(),
        "annual_earnings": annual_earnings,
        "monthly_earnings": json.dumps(monthly_earnings),
        "avg_month": avg_month,
        "today_sales": today_sales,
        "low_stock_items": low_stock_items,
        "total_customers": total_customers,
        "top_products": top_prods,
    }
    return Response(context)


class NotificationsView(APIView):

    def get_object(self, id):
        return get_object_or_404(Notifications, id=id, user=self.request.user)

    def get(self, request, id=None):
        if id:
            notification = self.get_object(id)
            notification.read = True
            notification.save()
            return Response(
                NotificationsSerializer(notification).data,
            )
        else:
            notifications = Notifications.objects.filter(
                read=False, user=request.user
            ).order_by("date")
            return Response(
                NotificationsSerializer(notifications, many=True).data,
            )

    def post(self, request):
        serializer = NotificationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, id):
        notification = self.get_object(id)
        serializer = NotificationsSerializer(
            notification, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
