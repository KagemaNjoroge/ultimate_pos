from .serializers import InventorySerializer
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from inventory.models import Inventory
from django.views.decorators.http import require_http_methods
from products.models import Product
from rest_framework.viewsets import ModelViewSet
from company.models import Branch


class InventoryViewSet(ModelViewSet):

    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


@login_required()
def index(request):
    inventory = Inventory.objects.all()
    context = {"inventory": inventory}
    return render(request, "inventory/inventory.html", context)


@login_required()
@require_http_methods(["GET"])
def add_inventory(request: HttpRequest) -> HttpResponse:

    products = Product.objects.exclude(inventory__isnull=False)
    branches = Branch.objects.all()
    return render(
        request,
        "inventory/inventory_add.html",
        {"products": products, "branches": branches},
    )


@login_required()
@require_http_methods(["GET"])
def update_inventory(request: HttpRequest, inventory_id: int) -> HttpResponse:
    inventory = get_object_or_404(Inventory, id=inventory_id)
    branches = Branch.objects.all()

    return render(
        request,
        "inventory/inventory_update.html",
        {"inventory": inventory, "branches": branches},
    )
