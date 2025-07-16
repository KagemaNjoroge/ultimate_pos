from rest_framework.serializers import ModelSerializer
from .models import Payment


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
