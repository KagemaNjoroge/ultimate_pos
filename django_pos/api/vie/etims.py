from ..ser.etims import (
    EtimsBranchSerializer,
    EtimsNoticeSerializer,
    ItemClassCodesSerializer,
    UnitsOfQuantitySerializer,
)
from rest_framework import viewsets
from etims.models import EtimsBranch, EtimsNotice, ItemClassCodes, UnitOfQuantity
from rest_framework import mixins
from drf_yasg.utils import swagger_auto_schema


class EtimsBranchViewSet(viewsets.ModelViewSet):
    queryset = EtimsBranch.objects.all()
    serializer_class = EtimsBranchSerializer

    @swagger_auto_schema(
        operation_summary="Get all branches",
        operation_description="Get all branches from the ETIMS database",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get a branch",
        operation_description="Get a branch from the ETIMS database",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a branch",
        operation_description="Create a branch in the ETIMS database",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a branch",
        operation_description="Update a branch in the ETIMS database",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a branch",
        operation_description="Delete a branch from the ETIMS database",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update a branch",
        operation_description="Partial update a branch in the ETIMS database",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class EtimsNoticeViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = EtimsNotice.objects.all()
    serializer_class = EtimsNoticeSerializer


class ItemClassCodesViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = ItemClassCodes.objects.all()
    serializer_class = ItemClassCodesSerializer


class UnitsOfQuantityViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = UnitOfQuantity.objects.all()
    serializer_class = UnitsOfQuantitySerializer
