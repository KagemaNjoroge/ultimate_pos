from .models import Customer

from .serializers import CustomerSerializer
from rest_framework.viewsets import ModelViewSet


class CustomerApiViewSet(ModelViewSet):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
