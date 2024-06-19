from etims.models import EtimsBranch, EtimsNotice, ItemClassCodes, UnitOfQuantity
from rest_framework import serializers


class EtimsBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtimsBranch
        fields = "__all__"


class EtimsNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtimsNotice
        fields = "__all__"


class ItemClassCodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemClassCodes
        fields = "__all__"


class UnitsOfQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfQuantity
        fields = "__all__"
