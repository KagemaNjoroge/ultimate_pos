from operator import le
import re
import stat
from turtle import st
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
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
        except Exception as e:
            pass

        # Check if a customer with the same attributes exists
        if Customer.objects.filter(**attributes).exists():
            messages.error(request, "Customer already exists!", extra_tags="warning")
            return redirect("customers:customers_add")

        try:
            # Create the customer
            new_customer = Customer.objects.create(**attributes)

            # If it doesn't exist, save it
            new_customer.save()

            messages.success(
                request,
                f'Customer: {attributes["first_name"]} {attributes["last_name"]}  created '
                f"successfully!",
                extra_tags="success",
            )
            return redirect("customers:customers_list")
        except Exception as e:
            messages.success(
                request, "There was an error during the creation!", extra_tags="danger"
            )

            return redirect("customers:customers_add")

    return render(request, "customers/customers_add.html", context=context, status=200)


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
    try:
        # Get the customer to delete
        customer = Customer.objects.get(id=customer_id)
        customer.delete()
        messages.success(
            request,
            "¡Customer: " + customer.get_full_name() + " deleted!",
            extra_tags="success",
        )
        return redirect("customers:customers_list")
    except Exception as e:
        print(e)
        messages.success(
            request,
            "There was an error deleting that customer, may be the customer has an existing sale record",
            extra_tags="danger",
        )

        return redirect("customers:customers_list")
