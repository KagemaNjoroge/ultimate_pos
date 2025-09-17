from rest_framework.viewsets import ModelViewSet
from .serializers import PhotoSerializer, Photo


class PhotoApiViewSet(ModelViewSet):

    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.all().order_by("-created_at")
