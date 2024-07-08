import json
from .serializers import InventorySerializer
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from inventory.models import Inventory
from pos.views import check_subscription
from products.models import Product


@check_subscription
@login_required(login_url="/users/login/")
def index(request):
    inventory = Inventory.objects.all()
    context = {"inventory": inventory, "active_icon": "inventory"}
    return render(request, "inventory/inventory.html", context)


@check_subscription
@login_required(login_url="/users/login/")
def add_inventory(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        # only products that are not in the inventory
        products = Product.objects.exclude(inventory__isnull=False)
        return render(request, "inventory/inventory_add.html", {"products": products})
    elif request.method == "POST":
        data = json.loads(request.body)
        serializer = InventorySerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(
                {"status": "success", "message": "Inventory added"}, safe=True
            )
        return JsonResponse(
            {
                "status": "error",
                "message": "Invalid data",
                "errors": serializer.errors,
            },
            status=400,
        )


@login_required(login_url="/users/login/")
@check_subscription
def update_inventory(request: HttpRequest, inventory_id: int) -> HttpResponse:
    inventory = get_object_or_404(Inventory, id=inventory_id)
    if request.method == "GET":
        return render(
            request, "inventory/inventory_update.html", {"inventory": inventory}
        )
    elif request.method == "POST":
        data = json.loads(request.body)
        serializer = InventorySerializer(inventory, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status": "success"}, safe=True)
        else:
            return JsonResponse({"status": "error"}, safe=True)
