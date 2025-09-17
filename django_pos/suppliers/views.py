from .models import Supplier
from .serializers import SupplierSerializer, Supplier
from rest_framework.viewsets import ModelViewSet


class SupplierApiViewSet(ModelViewSet):

    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
