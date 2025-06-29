from rest_framework.viewsets import ModelViewSet
from .serializers import PhotoSerializer, Photo


class PhotoApiViewSet(ModelViewSet):
    """
    API ViewSet for managing photos.
    """

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
