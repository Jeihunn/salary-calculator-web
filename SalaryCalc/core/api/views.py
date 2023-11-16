from rest_framework import generics
from rest_framework import permissions
from .serializers import SubscriberSerializer
from core.models import Subscriber


class SubscriberCreateAPIView(generics.CreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [permissions.AllowAny]