from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError
from .models import Sale, SaleItem


class SaleItemSerializer(ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ["id", "product", "quantity"]


class SaleSerializer(ModelSerializer):
    items = SaleItemSerializer(many=True, required=True)

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
            "total_tax",
        ]
        read_only_fields = ["receipt_is_printed"]

    # custom create method to handle nested serialization for items
    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        # validate - make sure there are no duplicate products in items_data [{product:1, quantity:2}, {product:1, quantity:3}] => error
        product_ids = [item["product"].id for item in items_data]
        if len(product_ids) != len(set(product_ids)):
            raise ValidationError("Duplicate products in sale items are not allowed.")

        items = []
        for item_data in items_data:
            item = SaleItem.objects.create(**item_data)
            items.append(item)

        sale = Sale.objects.create(**validated_data)
        sale.items.set([item.id for item in items])
        return sale
