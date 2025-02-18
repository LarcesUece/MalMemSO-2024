from ..utils import load_config, validate_config_data

# Load data from configuration file
config = load_config()

# Server authentication data
_REQUIRED_SERVER_KEYS = ["host", "port", "timeout", "endpoint"]
SERVER_DATA = config["server"]
validate_config_data(SERVER_DATA, _REQUIRED_SERVER_KEYS)

# Parser config data
PARSER_TOOL_OPTIONS = ["winpmem", "dumpit"]
PARSER_TOOL_DEFAULT = "winpmem"
PARSER_ARCH_OPTIONS = ["32bit", "64bit"]
PARSER_ARCH_MAPPING = {
    "32bit": "x86",
    "64bit": "x64",
}
PARSER_ARCH_DEFAULT = "64bit"
PARSER_DATA = {
    "tool_default": PARSER_TOOL_DEFAULT,
    "tool_options": PARSER_TOOL_OPTIONS,
    "arch_default": PARSER_ARCH_DEFAULT,
    "arch_options": PARSER_ARCH_OPTIONS,
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

TOOL_COMMANDS = {
    "dumpit": lambda tool_path, output_path: [tool_path, "/OUTPUT", output_path, "/Q"],
    "winpmem": lambda tool_path, output_path: [tool_path, output_path],
}
