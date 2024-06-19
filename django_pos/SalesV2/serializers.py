from rest_framework import serializers
from .models import Sale, SaleItem


class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = "__all__"


class SaleSerializer(serializers.ModelSerializer):
    sale_items = SaleItemSerializer(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = "__all__"
