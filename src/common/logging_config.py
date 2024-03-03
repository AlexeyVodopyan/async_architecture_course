# stdlib
import json
import logging

# thirdparty
from uvicorn.logging import DefaultFormatter

COMMON_RECORD_ATTRS = frozenset(
    (
        "args",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "lineno",
        "message",
        "module",
        "msecs",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "report",
        "color_message",
        "relativeCreated",
        "stack",
        "tags",
        "thread",
        "threadName",
        "stack_info",
        "asctime",
        "extra",
        "extra_info",
        "client_addr",
        "request_line",
        "status_code",
    )
)


class ConsoleDefaultFormatter(DefaultFormatter):
    """
    Console formatter
    """

    @staticmethod
    def _make_extra(record):
        """Pack extra dict"""

        extra = {}
        for key, val in record.__dict__.items():
            if key not in COMMON_RECORD_ATTRS:
                extra[key] = val
        return extra

    def format(self, record: logging.LogRecord) -> str:
        """Format log to proper format"""

        extra_info = self._make_extra(record)
        record.extra = ""
        if extra_info:
            record.extra = json.dumps(
                extra_info, ensure_ascii=False, default=str
            )
        text = super().format(record)
        if not record.extra and not record.exc_text:
            text = text[:-2]

        return text


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": ConsoleDefaultFormatter,
            "fmt": "{asctime} - {levelname} - {name}:{funcName}:{lineno} "
            "- {message} - {extra}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": False,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": "{asctime} - {levelname} - {client_addr} - {request_line} "
            "- {status_code}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {
            "handlers": ["access"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["default"],
    },
}
