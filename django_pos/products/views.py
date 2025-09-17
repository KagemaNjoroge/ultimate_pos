from .models import Category, Product, TaxGroup
from .serializers import CategorySerializer, ProductSerializer, TaxGroupSerializer
from rest_framework.viewsets import ModelViewSet


class TaxGroupApiViewSet(ModelViewSet):
    queryset = TaxGroup.objects.all()
    serializer_class = TaxGroupSerializer
    filterset_fields = ("name", "status", "tax_rate")


class CategoryApiViewSet(ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    filterset_fields = ("name", "status", "id")


class ProductApiViewSet(ModelViewSet):
    queryset = Product.objects.all()
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
