from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from core.constant import EXCLUDE_AUTH_PATH
from core.utils import path_is_excluded


class AuthenticateMiddleware(IsAuthenticated):
    def has_permission(self, request: Request, view):
        current_route = request.resolver_match.route
        if path_is_excluded(current_route, EXCLUDE_AUTH_PATH):
            return True
        else:
            return super().has_permission(request, view)
