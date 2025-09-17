from .models import Category, Product, TaxGroup
from .serializers import CategorySerializer, ProductSerializer, TaxGroupSerializer
from rest_framework.viewsets import ModelViewSet


class TaxGroupApiViewSet(ModelViewSet):

    serializer_class = TaxGroupSerializer
    filterset_fields = ("name", "status", "tax_rate")

    def get_queryset(self):
        return TaxGroup.objects.all().order_by("-created_at")


class CategoryApiViewSet(ModelViewSet):

    serializer_class = CategorySerializer

    filterset_fields = ("name", "status", "id")

    def get_queryset(self):
        return Category.objects.all().order_by("-created_at")


class ProductApiViewSet(ModelViewSet):

    serializer_class = ProductSerializer
    filterset_fields = (
        "name",
        "track_inventory",
        "status",
        "supplier",
        "id",
        "tax_group",
        "category",
    )

    def get_queryset(self):
        return Product.objects.all().order_by("-created_at")
