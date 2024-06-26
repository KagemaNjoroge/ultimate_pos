from django.shortcuts import render
from .models import Supplier


def index(request):
    suppliers = Supplier.objects.all()
    return render(request, "suppliers/index.html", {"suppliers": suppliers})


def add_supllier_template(request):
    return render(
        request,
        "suppliers/add_supplier.html",
    )
