from rest_framework import mixins

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


class CategoryView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk=pk)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, pk=None):
        if pk:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "Method PUT not allowed without pk"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

    def delete(self, request, pk=None):
        if pk:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"error": "Method DELETE not allowed without pk"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class ProductView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, id=None):
        if id:
            return self.list(request)
        else:
            pass

    def post(self, request):
        return self.create(request)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
