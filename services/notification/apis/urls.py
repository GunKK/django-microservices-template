from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .views import NotificationsViewSet

router = routers.DefaultRouter()
router = DefaultRouter()
router.register(r"v1/notifications", NotificationsViewSet, basename="notification")

urlpatterns = [
    path("", include(router.urls)),
]
