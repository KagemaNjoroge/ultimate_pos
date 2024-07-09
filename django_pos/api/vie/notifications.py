from ..ser.notifications import Notifications, NotificationsSerializer
from rest_framework import viewsets


class NotificationsViewset(viewsets.ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer
