from contextvars import ContextVar
from logging import Filter, LogRecord


class CorrelationIDFilter(Filter):
    """Adds correlation_id property provided by CorrelationIDMiddleware to logs."""

    def __init__(self, correlation_id_var: ContextVar, name: str = ""):
        super().__init__(name=name)
        self.correlation_id_var = correlation_id_var

    def filter(self, record: LogRecord) -> bool:
        record.correlation_id = self.correlation_id_var.get() or ""  # Using "" instead of None for better log repr.
        return True


def get_logging_config(log_level: str, correlation_id_var: ContextVar):
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "correlation_id": {
                "()": CorrelationIDFilter,
                "correlation_id_var": correlation_id_var,
            },
        },
        "formatters": {
            "default": {
                "format": "%(levelname)s: [%(correlation_id)s] %(asctime)s - %(module)s: %(message)s",
            },
        },
        "handlers": {
            "console": {
                "level": log_level,  # this level or higher goes to the console
                "class": "logging.StreamHandler",
                "formatter": "default",
                "filters": ["correlation_id"],
            },
        },
        "loggers": {
            "app": {  # Has to be the same name as our top module, hence  - app.
                "handlers": ["console"],
                "level": log_level,
                "propagate": False,
            },
            "root": {
                "level": log_level,
                "handlers": ["console"],
            },
        },
    }
