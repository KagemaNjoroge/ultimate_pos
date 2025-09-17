from rest_framework.serializers import ModelSerializer
from .models import Sale, SaleItem


class SaleItemSerializer(ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ["id", "product", "quantity"]


class SaleSerializer(ModelSerializer):
    items = SaleItemSerializer(many=True, required=False)

    class Meta:
        model = Sale
        fields = [
            "id",
            "created_at",
            "customer",
            "items",
            "receipt_is_printed",
            "discount",
            "sub_total",
            "grand_total",
        ]
        read_only_fields = ["receipt_is_printed"]
