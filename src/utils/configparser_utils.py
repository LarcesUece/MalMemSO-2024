from configparser import ConfigParser
from logging import error
from os.path import exists

from ..config.paths import INI_EXAMPLE_PATH, INI_PATH


def load_config(config_file: str = INI_PATH) -> ConfigParser:
    """Load a configuration file and return a ConfigParser object."""

    if not exists(config_file):

        if exists(INI_EXAMPLE_PATH):
            error_message = f"INI example file found at {INI_EXAMPLE_PATH}. Please rename it to config.ini and fill in the necessary values."
            error(error_message)
            raise FileExistsError(error_message)

        error_message = f"INI file not found at {config_file}"
        error(error_message)
        raise FileNotFoundError(error_message)

    config = ConfigParser()
    config.read(config_file)
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


# def validate_endpoint_data(data: dict) -> None:
#     if not data:
#         error_message = "Endpoint data is missing."
#         error(error_message)
#         raise ValueError(error_message)

#     for key in ["login", "upload", "response"]:
#         if key not in data:
#             error_message = f"Endpoint data is missing key: {key}"
#             error(error_message)
#             raise ValueError(error_message)

#         if not data[key]:
#             error_message = f"Endpoint data key is empty: {key}."
#             error(error_message)
#             raise ValueError(error_message)
