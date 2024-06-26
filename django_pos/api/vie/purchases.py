from ..ser.purchases import PurchaseSerializer, Purchase
from rest_framework import viewsets


class PurchaseViewset(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()
