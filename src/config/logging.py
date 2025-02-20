"""  
Logging Configuration  

This module configures logging for the application, ensuring logs are  
stored in the correct directory with the specified settings from  
predefined configuration constants.  

Functions:  
    - setup_logging(): Configures logging based on predefined settings.  
"""

from logging import basicConfig, error
from os.path import join

from ..config.config import (
    LOGGING_FILENAME,
    LOGGING_FORMAT,
    LOGGING_LEVEL,
    LOGGING_LEVEL_MAPPING,
)
from ..config.paths import LOGS_DIR


def setup_logging() -> None:
    """Configures logging for the application.

    Validates the given configuration and sets up logging with the
    specified settings from predefined constants.

    The function does not take any arguments and relies on the values
    from the configuration.
    """

    _validate_logging_config()

    filepath = join(LOGS_DIR, LOGGING_FILENAME + ".log")

    basicConfig(
        filename=filepath,
        level=LOGGING_LEVEL_MAPPING[LOGGING_LEVEL],
        format=LOGGING_FORMAT,
    )


def _validate_logging_config() -> None:
    """Validates the logging configuration values.

    Ensures that the required logging configuration values are provided,
    of the correct type and valid for setting up logging.

    Raises:
        ValueError: If any configuration value is missing, empty or
            invalid.
        TypeError: If any configuration value is not a string where
            expected.
    """

    if not LOGGING_FILENAME or not LOGGING_FORMAT or not LOGGING_LEVEL:
        error_message = "Logging configuration is missing required values."
        error(error_message)
        raise ValueError(error_message)

    if LOGGING_FILENAME == "" or LOGGING_FORMAT == "" or LOGGING_LEVEL == "":
        error_message = "Logging configuration values cannot be empty."
        error(error_message)
        raise ValueError(error_message)

    if not isinstance(LOGGING_FILENAME, str):
        error_message = "Logging filename must be a string."
        error(error_message)
        raise TypeError(error_message)

    if not isinstance(LOGGING_FORMAT, str):
        error_message = "Logging format must be a string."
        error(error_message)
        raise TypeError(error_message)

    if not isinstance(LOGGING_LEVEL, str):
        error_message = "Logging level must be a string."
        error(error_message)
        raise TypeError(error_message)

    if LOGGING_LEVEL not in LOGGING_LEVEL_MAPPING:
        error_message = "Invalid logging level provided."
        error(error_message)
        raise ValueError(error_message)
