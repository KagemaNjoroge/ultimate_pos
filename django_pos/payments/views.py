from .serializers import PaymentSerializer, Payment
from rest_framework.viewsets import ModelViewSet


class PaymentViewSet(ModelViewSet):
    """
    A viewset for viewing and editing payment instances.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_fields = ("sale", "payment_method", "status", "reference")

    def get_queryset(self):
        queryset = super().get_queryset()
        sale_id = self.request.query_params.get("sale_id", None)
        if sale_id is not None:
            queryset = queryset.filter(sale__id=sale_id)
        return queryset
