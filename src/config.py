from argparse import Namespace
from utils import (
    create_dir,
    load_config,
    setup_argparser,
    setup_logging,
    validate_endpoint_data,
    validate_server_data,
    BIN_PATH,
    LOGS_PATH,
    RAW_PATH,
    ZIP_PATH,
)

config = load_config()

# Server authentication data
SERVER_DATA = config["server"]
validate_server_data(SERVER_DATA)
ENDPOINT_DATA = config["server.endpoints"]
validate_endpoint_data(ENDPOINT_DATA)

# Parser config data
_PARSER_TOOL_OPTIONS = ["winpmem", "dumpit"]
_PARSER_TOOL_DEFAULT = "winpmem"
_PARSER_ARCH_OPTIONS = ["32bit", "64bit"]
_PARSER_ARCH_DEFAULT = "64bit"
PARSER_DATA = {
    "tool_default": _PARSER_TOOL_DEFAULT,
    "tool_options": _PARSER_TOOL_OPTIONS,
    "arch_default": _PARSER_ARCH_DEFAULT,
    "arch_options": _PARSER_ARCH_OPTIONS,
}

# Logging config data
# Logging level options: notset, debug, info, warn, warning, error, fatal, critical
_LOGGING_LEVEL = "info"
_LOGGING_FILENAME = "device"
_LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOGGING_DATA = {
    "level": _LOGGING_LEVEL,
    "filename": _LOGGING_FILENAME,
    "format": _LOGGING_FORMAT,
}


def initialize() -> Namespace:
    create_dir(BIN_PATH)
    create_dir(LOGS_PATH)
    create_dir(RAW_PATH)
    create_dir(ZIP_PATH)

    setup_logging(LOGGING_DATA)
    args = setup_argparser(PARSER_DATA)
    return args
