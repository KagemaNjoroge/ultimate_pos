from .serializers import InventorySerializer
from inventory.models import Inventory
from rest_framework.viewsets import ModelViewSet


class InventoryViewSet(ModelViewSet):

    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
