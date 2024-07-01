from django.shortcuts import render
from .models import Purchase, Branch, Product, Supplier
from django.shortcuts import get_object_or_404


def index(request):
    purchases = Purchase.objects.all()
    return render(
        request,
        "purchases/index.html",
        context={"purchases": purchases},
    )


def new_purchase(request):
    branches = Branch.objects.all()
    products = Product.objects.all()
    suppliers = Supplier.objects.all()
    status = []

    for i in Purchase.status.field.choices:
        status.append({"value": i[0], "name": i[-1]})

    return render(
        request,
        "purchases/new.html",
        context={
            "branches": branches,
            "products": products,
            "suppliers": suppliers,
            "status": status,
        },
    )


def purchase_details(request, id):
    purchase = get_object_or_404(Purchase, id=id)
    return render(
        request, "purchases/purchase-details.html", context={"purchase": purchase}
    )
