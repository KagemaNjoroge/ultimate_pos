from suppliers.serializers import SupplierSerializer
from rest_framework import viewsets
from suppliers.models import Supplier


class SupplierViewset(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
