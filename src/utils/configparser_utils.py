from configparser import ConfigParser
from logging import error
from os.path import exists

from utils.paths import INI_PATH


def load_config(config_file=INI_PATH):
    """Load a configuration file and return a ConfigParser object."""

    if not exists(config_file):
        error_message = f"INI file not found at {config_file}"
        error(error_message)
        raise FileNotFoundError(error_message)

    config = ConfigParser()
    config.read(config_file)
    return config
