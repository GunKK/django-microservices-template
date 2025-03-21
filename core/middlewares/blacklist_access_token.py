from django.core.cache import cache
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django_redis import get_redis_connection
from rest_framework import status


# check connection to redis
def tearDown(self):
    get_redis_connection("default").flushall()


class BlacklistAccessTokenMiddleware:
    """
    Middleware to check if the JWT token is blacklisted.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = self.__get_token_from_request(request)
        if token:
            if self.__is_token_blacklisted(token):
                return JsonResponse(
                    {
                        "status": False,
                        "message": _("Access token has been blacklisted!"),
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        response = self.get_response(request)
        return response

    def __get_token_from_request(self, request):
        """
        Extracts the JWT token from the request header.
        Assumes the token is in the Authorization header.
        """
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header[7:]
        return None

    def __is_token_blacklisted(self, token):
        """
        Checks if the token is in the Redis blacklist.
        """
        blacklist_key = f"blacklisted_access_token_{token}"
        return cache.get(blacklist_key) is not None
