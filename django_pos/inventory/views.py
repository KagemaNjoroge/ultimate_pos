from company.utils.branch_utils import get_current_branch
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
    current_branch = get_current_branch(request)

    # check if there is a branch query parameter
    if request.GET.get("branch"):
        branch_id = request.GET.get("branch")
        current_branch = Branch.objects.filter(id=branch_id).first()

    inventory = (
        Inventory.objects.filter(branch=current_branch)
        if current_branch
        else Inventory.objects.all()
    )
    context = {"inventory": inventory, "current_branch": current_branch}
    return render(request, "inventory/inventory.html", context)


@login_required()
@require_http_methods(["GET"])
def add_inventory(request: HttpRequest) -> HttpResponse:
    current_branch = get_current_branch(request)

    # check if there is a branch query parameter
    if request.GET.get("branch"):
        branch_id = request.GET.get("branch")
        current_branch = Branch.objects.filter(id=branch_id).first()

    if current_branch:
        # get only products that are not already in inventory for the current branch
        products = Product.objects.exclude(inventory__branch=current_branch)
    else:
        products = Product.objects.all()

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
