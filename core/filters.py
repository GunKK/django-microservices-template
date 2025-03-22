from django.db.models import Q
from django_filters import rest_framework as filters
from core.models import Notification

class NotificationFilter(filters.FilterSet):
    class Meta:
        model = Notification
        # define field search ex: name=xxx, id=yyy
        fields = {
            "is_read": ["exact"],
        }
