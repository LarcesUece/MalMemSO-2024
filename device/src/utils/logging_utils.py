from logging import (
    basicConfig,
    error,
    NOTSET,
    DEBUG,
    INFO,
    WARN,
    WARNING,
    ERROR,
    FATAL,
    CRITICAL,
)
from os.path import join

from .paths import LOGS_PATH
from .utils import create_dir


def setup_logging(data=None):
    """Setup logging configuration for the caller module."""

    _validate_data(data)
    create_dir(LOGS_PATH)

    filepath = join(LOGS_PATH, data["filename"] + ".log")

    basicConfig(
        filename=filepath,
        level=_get_level(data["level"]),
        format=data["format"],
    )


def _validate_data(data=None):
    if not data:
        error_message = "No logging data provided."
        error(error_message)
        raise ValueError(error_message)

    if not isinstance(data, dict):
        error_message = "Logging data must be a dictionary."
        error(error_message)
        raise TypeError(error_message)

    for key in ["level", "filename", "format"]:
        if key not in data:
            error_message = f"Missing key in data: {key}"
            error(error_message)
            raise ValueError(error_message)


def _get_level(level):
    match level:
        case "notset":
            return NOTSET
        case "debug":
            return DEBUG
        case "info":
            return INFO
        case "warn":
            return WARN
        case "warning":
            return WARNING
        case "error":
            return ERROR
        case "fatal":
            return FATAL
        case "critical":
            return CRITICAL
        case _:
            return INFO
