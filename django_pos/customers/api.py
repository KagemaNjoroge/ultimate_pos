from rest_framework.viewsets import ModelViewSet

from .models import Customer

from .serializers import CustomerSerializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
