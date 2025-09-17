from rest_framework import serializers
from .models import Product, Category, TaxGroup


class TaxGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxGroup
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            "supplier",
            "name",
            "description",
            "track_inventory",
            "photos",
            "display_image",
            "status",
            "category",
            "price",
            "tax_group",
            "tax_rate",
            "get_sku",
        )
