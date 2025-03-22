from django.db import DatabaseError
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.filters import NotificationFilter
from core.models import Notification
from core.paginators import CustomPaginator
from core.serializers.notification_serializers import NotificationSerializer
from core.utils import get_instance

from .documents import (
    create_notification_description,
    list_notifications_description,
    mark_all_as_read_notification_description,
    mark_as_read_notification_description,
    quantity_unread_notifications_description,
)


class NotificationsViewSet(viewsets.ViewSet):

    @extend_schema(**list_notifications_description)
    def list(self, request):
        filter_params = request.GET.dict()
        notifications = NotificationFilter(
            filter_params,
            queryset=Notification.objects.filter(user=request.user).prefetch_related(
                "user"
            ),
        )
        paginator = CustomPaginator()
        page = paginator.paginate_queryset(notifications.qs, request)
        serializer = NotificationSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(**create_notification_description)
    def create(self, request):
        data = request.data.get("data")
        notify_type = request.data.get("notify_type")
        notifications = Notification.objects.bulk_create(
            [
                Notification(
                    user_id=user,
                    data=data,
                    notify_type=notify_type,
                    is_read=False,
                )
                for user in request.data.get("user_ids")
            ]
        )

        return Response(
            {
                "status": True,
                "data": NotificationSerializer(notifications, many=True).data,
            },
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(**mark_all_as_read_notification_description)
    @action(detail=False, methods=["post"], url_path="mark_all_as_read")
    def mark_all_as_read(self, request):
        try:
            Notification.objects.filter(user=request.user).update(is_read=True)

            return Response(
                {
                    "status": True,
                    "data": "Successfully marked all notifications as read.",
                },
                status=status.HTTP_200_OK,
            )
        except DatabaseError as e:
            return Response(
                {"status": False, "message": f"Database error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"status": False, "message": f"Internal server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(**mark_as_read_notification_description)
    @action(detail=True, methods=["post"], url_path="mark_as_read")
    def mark_as_read(self, request, pk=None):
        try:
            notification = get_instance(Notification, pk)
            notification.is_read = True
            notification.save()
            return Response(
                {
                    "status": True,
                    "data": "Successfully marked notifications as read!",
                },
                status=status.HTTP_200_OK,
            )
        except DatabaseError as e:
            return Response(
                {"status": False, "message": f"Database error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"status": False, "message": f"Internal server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(**quantity_unread_notifications_description)
    @action(detail=False, methods=["get"], url_path="unread_notification_count")
    def unread_notification_count(self, request):
        unread_count = Notification.objects.filter(
            user=request.user, is_read=False
        ).count()

        return Response(
            {
                "status": True,
                "data": unread_count,
            },
            status=status.HTTP_200_OK,
        )
