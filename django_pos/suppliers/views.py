from django.shortcuts import render
from .models import Supplier
from company.models import Branch
from django.shortcuts import get_object_or_404


def index(request):
    suppliers = Supplier.objects.all()
    return render(request, "suppliers/index.html", {"suppliers": suppliers})


def add_supllier_template(request):
    branches = Branch.objects.all()
    return render(
        request, "suppliers/add_supplier.html", context={"branches": branches}
    )


def supplier_details(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    return render(request, "suppliers/supplier_details.html", {"supplier": supplier})
