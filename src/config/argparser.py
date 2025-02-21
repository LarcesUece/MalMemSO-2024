"""
Argument Parser Setup

This module configures and validates the command-line argument parsing 
for the application. It allows users to specify options such as the 
memory dump tool and system architecture, based on predefined 
configuration values.

Functions:
    - setup_argparser(): Initializes and configures the argument parser.
"""

from argparse import ArgumentParser, Namespace
from logging import error, info

from ..config.config import (
    PARSER_ARCH_DEFAULT,
    PARSER_ARCH_OPTIONS,
    PARSER_TOOL_DEFAULT,
    PARSER_TOOL_OPTIONS,
)


def setup_argparser() -> Namespace:
    """Setup the argument parser for the application.

    Configures an ArgumentParser using predefined constants, which
    define options for selecting the memory dump tool and system
    architecture.

    Returns:
        argparser.Namespace: The parsed command-line arguments,
        containing values for 'tool' and 'arch' options.
    """

    _validate_parser_config()

    parser_description = "Memory dump extraction, compression and malware remediation"
    parser_args = {
        ("-t", "--tool"): {
            "type": str,
            "choices": PARSER_TOOL_OPTIONS,
            "default": PARSER_TOOL_DEFAULT,
            "help": "Memory dump extraction tool to be used",
        },
        ("-a", "--arch"): {
            "type": str,
            "choices": PARSER_ARCH_OPTIONS,
            "default": PARSER_ARCH_DEFAULT,
            "help": "Architecture of the system to be analyzed",
        },
    }

    parser = ArgumentParser(description=parser_description)
    for arg_name, arg_data in parser_args.items():
        if isinstance(arg_name, tuple):
            parser.add_argument(*arg_name, **arg_data)
        else:
            parser.add_argument(arg_name, **arg_data)
    args = parser.parse_args()

    info("Argument parser setup complete.")

    return args


def _validate_parser_config() -> None:
    """Validate the parser configuration.

    Ensures the necessary values for the argument parser are defined
    and have the correct types. This includes checking for required
    keys, valid default values and ensuring that options are lists and
    defaults are strings.

    Raises:
        ValueError: If any required value is missing, empty, or invalid.
        TypeError: If any configuration value is of an incorrect type.
    """

    if (
        not PARSER_TOOL_OPTIONS
        or not PARSER_ARCH_OPTIONS
        or not PARSER_TOOL_DEFAULT
        or not PARSER_ARCH_DEFAULT
    ):
        error_message = "Parser configuration is missing required values."
        error(error_message)
        raise ValueError(error_message)

    if (
        PARSER_TOOL_DEFAULT == ""
        or PARSER_ARCH_DEFAULT == ""
        or len(PARSER_TOOL_OPTIONS) == 0
        or len(PARSER_ARCH_OPTIONS) == 0
    ):
        error_message = "Parser configuration values cannot be empty."
        error(error_message)
        raise ValueError(error_message)

    if not isinstance(PARSER_TOOL_OPTIONS, list) or not isinstance(
        PARSER_ARCH_OPTIONS, list
    ):
        error_message = "Parser options must be lists."
        error(error_message)
        raise TypeError(error_message)

    if not isinstance(PARSER_TOOL_DEFAULT, str) or not isinstance(
        PARSER_ARCH_DEFAULT, str
    ):
        error_message = "Parser default values must be strings."
        error(error_message)
        raise TypeError(error_message)

    if PARSER_TOOL_DEFAULT not in PARSER_TOOL_OPTIONS:
        error_message = "Invalid default tool provided."
        error(error_message)
        raise ValueError(error_message)

    if PARSER_ARCH_DEFAULT not in PARSER_ARCH_OPTIONS:
        error_message = "Invalid default architecture provided."
        error(error_message)
        raise ValueError(error_message)

    info("Parser configuration validated.")
