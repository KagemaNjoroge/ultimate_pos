from .models import Photo
from rest_framework import serializers


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["image_url"] = instance.image.url if instance.image else None
        return representation
