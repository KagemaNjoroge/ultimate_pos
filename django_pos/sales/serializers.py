from rest_framework.serializers import ModelSerializer
from .models import Sale


class SaleSerializer(ModelSerializer):
    class Meta:
        model = Sale
        fields = [
            "id",
            "created_at",
            "customer",
            "sub_total",
            "grand_total",
            "receipt_is_printed",
            "discount",
        ]
        read_only_fields = ["id", "created_at", "receipt_is_printed"]
        extra_kwargs = {
            "customer": {"required": True},
            "sub_total": {"required": True},
            "grand_total": {"required": True},
            "discount": {"required": False, "default": 0},
        }
