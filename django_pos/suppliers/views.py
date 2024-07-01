from django.shortcuts import render
from .models import Supplier
from company.models import Branch


def index(request):
    suppliers = Supplier.objects.all()
    return render(request, "suppliers/index.html", {"suppliers": suppliers})


def add_supllier_template(request):
    branches = Branch.objects.all()
    return render(
        request, "suppliers/add_supplier.html", context={"branches": branches}
    )
