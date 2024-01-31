from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from inventory.models import Inventory


# Create your views here.
def index(request):
    inventory = Inventory.objects.all()
    context = {
        'inventory': inventory,
        "active_icon": "inventory"
    }
    return render(request, 'inventory/inventory.html', context)


def add_inventory(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'inventory/inventory_add.html')

