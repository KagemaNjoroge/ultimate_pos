import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from sales.models import Sale
from .models import Customer


# TODO: Remove duplicate code


@login_required(login_url="/accounts/login/")
def customers_list_view(request: HttpRequest) -> HttpResponse:
    context = {"active_icon": "customers", "customers": Customer.objects.all()}
    return render(request, "customers/customers.html", context=context)


@login_required(login_url="/accounts/login/")
def customers_add_view(request: HttpRequest) -> HttpResponse:
    context = {
        "active_icon": "customers",
    }

    if request.method == "POST":
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
        # try to get the photo
        try:
            attributes["photo"] = request.FILES["photo"]
        except KeyError:
            pass

        # Check if a customer with the same attributes exists
        if Customer.objects.filter(**attributes).exists():
            # return JsonResponse
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Customer with the same attributes already exists",
                },
                status=400,
            )

        try:
            # Create the customer
            new_customer = Customer.objects.create(**attributes)

            # If it doesn't exist, save it
            new_customer.save()
            return JsonResponse(
                {"status": "success", "message": "Customer added successfully!"},
                status=200,
            )

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    elif request.method == "GET":

        return render(
            request, "customers/customers_add.html", context=context, status=200
        )
    else:
        return JsonResponse(
            {"status": "error", "message": "Method not allowed!"}, status=405
        )


@login_required(login_url="/accounts/login/")
def customers_update_view(request: HttpRequest, customer_id: str) -> HttpResponse:
    """
    Args:
        request: HttpRequest Object
        customer_id : The customer's ID that will be updated
    """
    if request.method == "GET":
        customer = get_object_or_404(Customer, id=customer_id)

        context = {
            "active_icon": "customers",
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


@login_required(login_url="/accounts/login/")
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


@login_required(login_url="/accounts/login/")
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
        "active_icon": "customers",
        "customer": customer,
        "sales": sales,
        "purchases_this_month": purchases_this_month.count(),
        "amount_spent_this_month": amount_spent_this_month,
        "amount_spent_this_year": amount_spent_this_year,
    }
    return render(
        request, "customers/customer_profile.html", context=context, status=200
    )
