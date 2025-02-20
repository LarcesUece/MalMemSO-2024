from configparser import ConfigParser
from logging import error
from os.path import exists

from ..config.paths import INI_PATH


def load_config() -> ConfigParser:
    """Load a configuration file and return a ConfigParser object."""

    if not exists(INI_PATH):
        error_message = f"INI file not found at '{INI_PATH}'."
        error(error_message)
        raise FileNotFoundError(error_message)

    config = ConfigParser()
    config.read(INI_PATH)
    return config


def validate_config_data(data: dict, required_keys: list) -> None:
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
