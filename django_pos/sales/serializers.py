from rest_framework.serializers import ModelSerializer
from .models import Sale


class SaleSerializer(ModelSerializer):
    class Meta:
        model = Sale
        fields = [
            "id",
            "date_added",
            "customer",
            "sub_total",
            "grand_total",
            "tax_amount",
            "tax_percentage",
            "amount_payed",
            "amount_change",
            "receipt_is_printed",
            "discount",
        ]
        read_only_fields = ["id", "date_added", "receipt_is_printed"]
        extra_kwargs = {
            "customer": {"required": True},
            "sub_total": {"required": True},
            "grand_total": {"required": True},
            "tax_amount": {"required": True},
            "tax_percentage": {"required": True},
            "amount_payed": {"required": True},
            "amount_change": {"required": True},
        }
