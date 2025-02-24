"""
Handles loading and validating configuration files.

Functions:
    load_config: Loads the configuration from an INI file.
    validate_config_data: Validates configuration data against required 
        keys.
"""

from configparser import ConfigParser
from logging import error, info
from os.path import exists

from ..config.paths import INI_PATH


def load_config() -> ConfigParser:
    """Loads configuration from INI file.

    Returns:
        configparser.ConfigParser: Parsed configuration object.
    """

    if not exists(INI_PATH):
        error_message = f"INI file not found at '{INI_PATH}'."
        error(error_message)
        raise FileNotFoundError(error_message)

    config = ConfigParser()
    config.read(INI_PATH)

    info("Configuration loaded successfully.")

    return config


def validate_config_data(data: dict, required_keys: list) -> None:
    """Validates that config data contains required keys.

    Args:
        data (dict): Configuration data.
        required_keys (list): Keys that must be present.
    """

    if not data:
        error_message = "Config data is missing."
        error(error_message)
        raise ValueError(error_message)

    for key in required_keys:
        if key not in data:
            error_message = f"Config data is missing key: {key}"
            error(error_message)
            raise ValueError(error_message)

        if not data[key]:
            error_message = f"Config data key is empty: {key}."
            error(error_message)
            raise ValueError(error_message)

    info("Configuration data validated.")
