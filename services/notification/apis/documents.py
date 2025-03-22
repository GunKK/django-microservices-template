from drf_spectacular.utils import OpenApiParameter, OpenApiResponse
from rest_framework.exceptions import NotFound

from core.serializers.notification_serializers import NotificationSerializer

list_notifications_description = {
    "summary": "Get list of notifications",
    "description": "get list of notifications and filter eg: http://localhost:9000/api/v1/notifications/?page=1&page_size=5",
    "parameters": [
        OpenApiParameter(
            "page", int, required=False, default=1, description="Page number"
        ),
        OpenApiParameter(
            "page_size",
            int,
            required=False,
            default=5,
            description="Number of projects per page.",
        ),
    ],
    "responses": {200: NotificationSerializer(many=True)},
}

create_notification_description = {
    "summary": "Create notification",
    "description": "Create notification",
    "responses": {200: NotificationSerializer(many=True)},
}

mark_all_as_read_notification_description = {
    "summary": "Mark all read notification by current user",
    "description": "Mark all read notification by current user",
    "responses": {200: {"data": "Successfully marked all notifications as read."}},
}

mark_as_read_notification_description = {
    "parameters": [
        OpenApiParameter(
            "id",
            type=int,
            location=OpenApiParameter.PATH,
            description="ID of the notification",
        ),
    ],
    "summary": "mark as read a notification by current user",
    "description": "mark as read a notification by current user",
    "responses": {200: {"data": "Successfully marked notifications as read!"}},
}

quantity_unread_notifications_description = {
    "summary": "Get quantity of unread notifications",
    "description": "get quantity of unread notifications",
    "responses": {200: int},
}
