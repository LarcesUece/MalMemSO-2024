"""
Configuration loader for the application.

Loads service, parser and logging configurations.
"""

from logging import CRITICAL, DEBUG, ERROR, FATAL, INFO, NOTSET, WARN, WARNING

from ..config.configparser import load_config, validate_config_data

# Load data from configuration file
config = load_config()

# MalMemSO service connection info
_REQUIRED_CONFIG_KEYS = ["host", "port", "timeout"]
_REQUIRED_CONFIG_ENDPOINTS = ["upload", "response"]
SERVICE_DATA = config["service"]
ENDPOINT_DATA = config["service.endpoints"]
validate_config_data(SERVICE_DATA, _REQUIRED_CONFIG_KEYS)
validate_config_data(ENDPOINT_DATA, _REQUIRED_CONFIG_ENDPOINTS)

# Parser config data
PARSER_TOOL_OPTIONS = ["winpmem", "dumpit"]
PARSER_TOOL_DEFAULT = "winpmem"
PARSER_ARCH_OPTIONS = ["32bit", "64bit"]
PARSER_ARCH_MAPPING = {
    "32bit": "x86",
    "64bit": "x64",
}
PARSER_ARCH_DEFAULT = "64bit"

# Logging config data
# Logging level options: notset, debug, info, warn, warning, error, fatal, critical
LOGGING_LEVEL = "info"
LOGGING_LEVEL_MAPPING = {
    "notset": NOTSET,
    "debug": DEBUG,
    "info": INFO,
    "warn": WARN,
    "warning": WARNING,
    "error": ERROR,
    "fatal": FATAL,
    "critical": CRITICAL,
}
LOGGING_FILENAME = "device"
LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

TOOL_COMMANDS = {
    "dumpit": lambda tool_path, output_path: [tool_path, "/OUTPUT", output_path, "/Q"],
    "winpmem": lambda tool_path, output_path: [tool_path, output_path],
}
