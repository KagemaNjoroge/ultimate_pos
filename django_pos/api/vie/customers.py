from rest_framework import viewsets

from ..ser.customers import Customer, CustomerSerializer


class CustomersViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
