from django.shortcuts import render
from .models import Supplier
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required()
def index(request):
    suppliers = Supplier.objects.all()
    return render(request, "suppliers/index.html", {"suppliers": suppliers})


@login_required()
def add_supllier_template(request):    
    return render(
        request, "suppliers/add_supplier.html"
    )


@login_required()
def supplier_details(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    return render(request, "suppliers/supplier_details.html", {"supplier": supplier})
