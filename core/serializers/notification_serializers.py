from rest_framework import serializers

from core.models import Notification

from .user_serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = "__all__"
        ordering = ["id"]
