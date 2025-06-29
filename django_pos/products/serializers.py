from rest_framework import serializers
from .models import Product, Category
from utils.models import Photo


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    selected_photos = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )

    class Meta:
        model = Product
        fields = "__all__"

    def update(self, instance, validated_data):
        # Handle photos separately
        selected_photos_str = validated_data.pop("selected_photos", None)

        # Update the product with other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle photos if provided
        if selected_photos_str is not None:
            if selected_photos_str.strip():
                # Parse the photo IDs
                photo_ids = [
                    int(id.strip())
                    for id in selected_photos_str.split(",")
                    if id.strip().isdigit()
                ]
                # Get the photo objects
                photos = Photo.objects.filter(id__in=photo_ids)
                # Set the photos for this product
                instance.photos.set(photos)
            else:
                # Clear all photos if empty string
                instance.photos.clear()

        return instance
