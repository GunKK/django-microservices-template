from django.urls import include, path
from rest_framework import routers

from .views import (
    AuthenViewSet,
    CustomTokenRefreshView,
)


router = routers.DefaultRouter()
router.register(r"v1/auth", AuthenViewSet, basename="auth")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"v1/auth/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]
