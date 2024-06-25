from django.shortcuts import render
from rest_framework import viewsets
from .models import Supplier
from .serializers import SupplierSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


def index(request):
    suppliers = Supplier.objects.all()
    return render(request, "suppliers/index.html", {"suppliers": suppliers})


def add_supllier_template(request):
    return render(
        request,
        "suppliers/add_supplier.html",
    )
