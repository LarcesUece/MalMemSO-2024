"""
Configuration Parser

This module provides functions to load and validate configuration data 
from an INI file. It utilizes the ConfigParser class to read and parse 
the configuration file, and ensures that required keys are present in 
the parsed data.

Functions:
    - load_config(): Loads the configuration from the specified INI 
        file and returns a ConfigParser object.
    - validate_config_data(data, required_keys): Validates the parsed 
        configuration data, ensuring the presence and non-emptiness of 
        required keys.
"""

from configparser import ConfigParser
from logging import error, info
from os.path import exists

from ..config.paths import INI_PATH


def load_config() -> ConfigParser:
    """Load and return the configuration from the INI file.

    Reads the INI file from the predefined path and returns a
    ConfigParser object containing the parsed configuration.

    Returns:
        configparser.ConfigParser: The parsed configuration as a
            ConfigParser object.

    Raises:
        FileNotFoundError: If the INI file is not found at the
            predefined path.
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
    """Validates the configuration data.

    Ensures that the given configuration data contains all required
    keys and that none of the values are empty.

    Args:
        data (dict): The parsed configuration data to be validated.
        required_keys (list): A list of keys that must be present in
            the configuration data.

    Raises:
        ValueError: If the data is missing any required keys or if
            any required key has an empty value.
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
