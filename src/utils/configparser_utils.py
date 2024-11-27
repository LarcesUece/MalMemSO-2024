from configparser import ConfigParser
from logging import error
from os.path import exists

from utils.paths import INI_PATH, INI_EXAMPLE_PATH


def load_config(config_file=INI_PATH):
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
