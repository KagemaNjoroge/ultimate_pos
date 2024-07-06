import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from pos.views import check_subscription
from sales.models import Sale
from .models import Customer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from .serializers import CustomerSerializer
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer


@login_required(login_url="/users/login/")
@check_subscription
def customers_list_view(request: HttpRequest) -> HttpResponse:
    context = {"customers": Customer.objects.all()}
    return render(request, "customers/customers.html", context=context)


@login_required(login_url="/users/login/")
@check_subscription
@api_view(["GET", "POST"])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def customers_add_view(request) -> Response:

    if request.method == "POST":
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "message": "Customer added successfully!"},
                status=201,
            )
        return Response({"status": "error", "message": serializer.errors}, status=400)

    elif request.method == "GET":
        # This part remains unchanged, serving HTML for GET requests
        if request.accepted_renderer.format == "html":
            return render(
                request,
                template_name="customers/customers_add.html",
                status=200,
            )
        else:
            # For non-HTML requests, inform about the method not being allowed
            return Response(
                {"status": "error", "message": "Method not allowed!"}, status=405
            )


@login_required(login_url="/users/login/")
@check_subscription
def customers_update_view(request: HttpRequest, customer_id: str) -> HttpResponse:
    """
    Args:
        request: HttpRequest Object
        customer_id : The customer's ID that will be updated
    """
    if request.method == "GET":
        customer = get_object_or_404(Customer, id=customer_id)

        context = {
            "customer": customer,
        }
        return render(
            request, "customers/customers_update.html", context=context, status=200
        )

    if request.method == "POST":
        try:
            # Save the POST arguments
            data = request.POST

            attributes = {
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "address": data["address"],
                "email": data["email"],
                "phone": data["phone"],
                "kra_pin": data["kra_pin"],
            }

            customer = get_object_or_404(Customer, id=customer_id)
            # Update the customer
            customer.first_name = attributes["first_name"]
            customer.last_name = attributes["last_name"]
            customer.address = attributes["address"]
            customer.email = attributes["email"]
            customer.phone = attributes["phone"]
            customer.kra_pin = attributes["kra_pin"]
            if "photo" in request.FILES:

                customer.photo = request.FILES["photo"]
            # Save the customer
            customer.save()
            return JsonResponse(
                {"status": "success", "message": "Customer updated successfully!"},
                status=200,
            )

        except Exception as e:

            return JsonResponse({"status": "error", "message": str(e)})


@login_required(login_url="/users/login/")
@check_subscription
def customers_delete_view(request: HttpRequest, customer_id: str) -> HttpResponse:
    """
    Args:
        request: HttpRequest Object
        customer_id : The customer's ID that will be deleted
    """
    if request.method == "DELETE":
        try:
            # Get the customer to delete
            customer = get_object_or_404(Customer, id=customer_id)
            customer.delete()
            return JsonResponse(
                {"status": "success", "message": "Customer deleted successfully!"},
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        # not allowed
        return JsonResponse(
            {"status": "error", "message": "Method not allowed!"}, status=405
        )


@login_required(login_url="/users/login/")
@check_subscription
def customer_profile(request: HttpRequest, id: str) -> HttpResponse:
    customer = get_object_or_404(Customer, id=id)
    # 10 recent purchase histories
    sales = Sale.objects.filter(customer=customer).order_by("-date_added")[:10]

    purchases_this_month = Sale.objects.filter(
        customer=customer, date_added__month=datetime.datetime.now().month
    )
    amount_spent_this_month = sum([sale.grand_total for sale in purchases_this_month])
    amount_spent_this_year = sum(
        [
            sale.grand_total
            for sale in Sale.objects.filter(
                customer=customer, date_added__year=datetime.datetime.now().year
            )
        ]
    )
    # TODO: Add customers most purchased product

    context = {
     
        "customer": customer,
        "sales": sales,
        "purchases_this_month": purchases_this_month.count(),
        "amount_spent_this_month": amount_spent_this_month,
        "amount_spent_this_year": amount_spent_this_year,
    }
    return render(
        request, "customers/customer_profile.html", context=context, status=200
    )
