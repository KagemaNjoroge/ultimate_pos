from rest_framework import viewsets
from .serializers import SaleSerializer, SaleItemSerializer
from .models import Sale, SaleItem


class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
