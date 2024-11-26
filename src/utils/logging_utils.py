from inspect import stack
from logging import INFO, basicConfig, error
from os import makedirs
from os.path import join, exists, splitext

from utils.paths import LOGS_PATH, SRC_PATH

DEFAULT_FILENAME = "default"
DEFAULT_LEVEL = INFO
DEFAULT_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


def setup_logging(custom_filename=False, level=DEFAULT_LEVEL, format=DEFAULT_FORMAT):
    """Setup logging configuration for the caller module."""

    if not exists(LOGS_PATH):
        try:
            makedirs(LOGS_PATH)
        except:
            error_message = f"Failed to create logs directory at {LOGS_PATH}"
            error(error_message)
            raise PermissionError(error_message)

    if custom_filename:
        caller_file = stack()[1].filename
        filename = _get_log_filename(caller_file)
    else:
        filename = DEFAULT_FILENAME

    filepath = join(LOGS_PATH, filename + ".log")

    basicConfig(
        filename=filepath,
        level=level,
        format=format,
    )


def _get_log_filename(caller_file=None):
    """Generate a log filename based on the caller file path."""

    if not caller_file:
        error_message = "Caller file not provided"
        error(error_message)
        raise ValueError(error_message)

    log_filename = caller_file.replace(SRC_PATH, "")
    log_filename = splitext(log_filename)[0]
    log_filename = log_filename.replace("/", "_")
    log_filename = log_filename.replace("\\", "_")
    log_filename = log_filename[1:] if log_filename[0] == "_" else log_filename

    return log_filename
