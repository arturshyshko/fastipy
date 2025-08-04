import typing as t
from contextvars import ContextVar
from unittest.mock import MagicMock

from core.middleware.logging import CorrelationIDMiddleware


def test_loggin_middleware(rf):
    get_response = MagicMock()
    cid: ContextVar[t.Optional[str]] = ContextVar("test_correlation_middleware", default=None)
    middleware = CorrelationIDMiddleware(
        get_response,
        header_name="X-Dummy-Request-ID",
        storage=cid,
    )
    request = rf.get("/", headers={"X-Dummy-Request-ID": "123"})
    middleware(request)

    assert cid.get() == "123"
