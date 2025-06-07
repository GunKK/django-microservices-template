from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import AccessToken

from core.constant import EXCLUDE_AUTH_PATH
from core.utils import get_access_token_from_request, path_is_excluded


class TokenVersionMiddleware(BasePermission):
    def has_permission(self, request: Request, view):
        current_route = request.resolver_match.route
        if path_is_excluded(current_route, EXCLUDE_AUTH_PATH):
            return True
        access_token = AccessToken(get_access_token_from_request(request))
        token = access_token.payload.get("token_version", None)
        if request.user and request.user.is_token_version_valid(token):
            return True
        raise AuthenticationFailed("Token is invalid due to version mismatch!")
