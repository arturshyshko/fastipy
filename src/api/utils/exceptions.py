from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

from core.constants.exceptions import PlaceholderException


def placeholder_exception_handler(exc, context):
    if isinstance(exc, PlaceholderException):
        exc = APIException(detail=str(exc))
        exc.status_code = status.HTTP_400_BAD_REQUEST

    response = exception_handler(exc, context)

    return response
