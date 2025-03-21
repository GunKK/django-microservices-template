from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    error_messages = {
        status.HTTP_401_UNAUTHORIZED: {
            "status": False,
            "message": _("Authentication credentials were not provided."),
        },
        status.HTTP_403_FORBIDDEN: {
            "status": False,
            "message": "Unfortunately, you do not have permission.",
        },
        status.HTTP_404_NOT_FOUND: {
            "status": False,
            "message": "The requested resource could not be found.",
        },
        # status.HTTP_500_INTERNAL_SERVER_ERROR: {
        #     "status": False,
        #     "message": "An unexpected error occurred on the server.",
        # },
    }

    if response is not None and response.status_code in error_messages:
        return Response(
            error_messages[response.status_code], status=response.status_code
        )

    return response
