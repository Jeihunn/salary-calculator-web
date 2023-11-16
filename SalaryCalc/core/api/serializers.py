from rest_framework import serializers
from core.models import Subscriber


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ("email", "subscription_status")
        
        read_only_fields = ("subscription_status",)