import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from sales.models import Sale
from .models import Customer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from .serializers import CustomerSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.viewsets import ModelViewSet


class CustomerApiViewSet(ModelViewSet):
    """
    API ViewSet for Customer model.
    Provides CRUD operations for customers.
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


@login_required(login_url="/users/login/")
@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def customers_list_view(request: HttpRequest) -> HttpResponse:
    # new customers - last 30 days -  to cache
    new_customers = Customer.objects.filter(
        created_at__gte=datetime.datetime.now() - datetime.timedelta(days=30)
    ).count()

    context = {"customers": Customer.objects.all(), "new_customers": new_customers}
    return render(request, "customers/customers.html", context=context)


@login_required(login_url="/users/login/")
@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def customers_add_view(request) -> Response:
    if request.accepted_renderer.format == "html":
        return render(
            request,
            template_name="customers/customers_add.html",
            status=200,
        )
    else:
        return Response(
            {"message": "This endpoint only supports HTML rendering."},
            status=400,
        )


@login_required(login_url="/users/login/")
@api_view(["GET"])
def customers_update_view(request: HttpRequest, customer_id: str) -> HttpResponse:
    customer = get_object_or_404(Customer, id=customer_id)

    context = {
        "customer": customer,
    }
    return render(
        request, "customers/customers_update.html", context=context, status=200
    )


@login_required(login_url="/users/login/")
def customer_profile(request: HttpRequest, id: str) -> HttpResponse:
    customer = get_object_or_404(Customer, id=id)

    # Current date for calculations
    now = datetime.datetime.now()
    current_month = now.month
    current_year = now.year

    # 10 recent purchase histories
    sales = Sale.objects.filter(customer=customer).order_by("-date_added")[:10]

    # Monthly statistics
    purchases_this_month = Sale.objects.filter(
        customer=customer,
        date_added__month=current_month,
        date_added__year=current_year,
    )

    # Yearly statistics
    purchases_this_year = Sale.objects.filter(
        customer=customer, date_added__year=current_year
    )

    # Calculate amounts
    amount_spent_this_month = sum([sale.grand_total for sale in purchases_this_month])
    amount_spent_this_year = sum([sale.grand_total for sale in purchases_this_year])

    # Additional statistics for enhanced profile
    total_purchases = Sale.objects.filter(customer=customer).count()
    total_amount_all_time = sum(
        [sale.grand_total for sale in Sale.objects.filter(customer=customer)]
    )

    # Calculate average purchase amount
    average_purchase_amount = (
        total_amount_all_time / total_purchases if total_purchases > 0 else 0
    )

    # Last purchase date
    last_purchase = (
        Sale.objects.filter(customer=customer).order_by("-date_added").first()
    )
    last_purchase_date = last_purchase.date_added if last_purchase else None

    # Customer lifetime value and engagement metrics
    customer_since = customer.created_at if hasattr(customer, "created_at") else None

    # Most recent transaction status
    recent_transactions_count = sales.count()

    context = {
        "customer": customer,
        "sales": sales,
        "purchases_this_month": purchases_this_month.count(),
        "amount_spent_this_month": amount_spent_this_month,
        "amount_spent_this_year": amount_spent_this_year,
        "total_purchases": total_purchases,
        "total_amount_all_time": total_amount_all_time,
        "average_purchase_amount": average_purchase_amount,
        "last_purchase_date": last_purchase_date,
        "customer_since": customer_since,
        "recent_transactions_count": recent_transactions_count,
    }
    return render(
        request, "customers/customer_profile.html", context=context, status=200
    )


@login_required(login_url="/users/login/")
def import_customers(request: HttpRequest) -> HttpResponse:
    return render(request, template_name="customers/import_customers.html")
