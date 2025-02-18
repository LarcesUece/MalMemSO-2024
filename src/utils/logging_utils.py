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

from ..config.paths import LOGS_DIR
from .utils import create_dir


def setup_logging(data: dict) -> None:
    """Setup logging configuration for the caller module."""

    _validate_data(data)
    create_dir(LOGS_DIR)

    filepath = join(LOGS_DIR, data["filename"] + ".log")

    basicConfig(
        filename=filepath,
        level=_get_level(data["level"]),
        format=data["format"],
    )


def _validate_data(data: dict) -> None:
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


def _get_level(level: str) -> int:
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
