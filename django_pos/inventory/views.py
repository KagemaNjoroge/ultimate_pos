from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
import json
from inventory.models import Inventory
from products.models import Product


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
        products = Product.objects.all()
        return render(request, 'inventory/inventory_add.html', {"products": products})
    elif request.method == 'POST':
        data = json.loads(request.body)
        product_id = int(data['product'])
        quantity = int(data['quantity'])

        product = Product.objects.get(id=product_id)
        inventory = Inventory(product=product, quantity=quantity)
        inventory.save()
        return JsonResponse({"status": "success"}, safe=True)
