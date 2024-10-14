import typing as t
from contextvars import ContextVar

from django.conf import settings

correlation_id: ContextVar[t.Optional[str]] = ContextVar("correlation_id", default=None)


class CorrelationIDMiddleware:
    """Generate request' correlation ID which is then accessed by app logger and appended to all logs.

    Looks for a value in <header_name> request header and set correlation_id contextvar to that value.
    """

    def __init__(self, get_response, header_name: t.Optional[str] = None, storage: ContextVar = correlation_id):
        self.get_response = get_response
        self.header_name = header_name or getattr(settings, "CORRELATION_ID_HEADER", "X-Request-ID")
        self.storage = storage

    def __call__(self, request):
        self.storage.set(request.headers.get(self.header_name))
        response = self.get_response(request)
        return response
