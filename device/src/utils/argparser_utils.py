from argparse import ArgumentParser
from logging import error


def setup_argparser(data=None):
    """Setup the argument parser for the given module."""

    _validate_data(data)

    parser_description = "Memory dump extraction, compression and malware remediation"
    parser_args = {
        ("-t", "--tool"): {
            "type": str,
            "choices": data["tool_options"],
            "default": data["tool_default"],
            "help": "Memory dump tool to be used",
        },
        ("-a", "--arch"): {
            "type": str,
            "choices": data["arch_options"],
            "default": data["arch_default"],
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
    return args


def _validate_data(data=None):
    """Validate the data dictionary."""

    if not data:
        error_message = "Data not provided."
        error(error_message)
        raise ValueError(error_message)

    if not isinstance(data, dict):
        error_message = "Data must be a dictionary."
        error(error_message)
        raise TypeError(error_message)

    for key in ["tool_options", "tool_default", "arch_options", "arch_default"]:
        if key not in data:
            error_message = f"Missing key in data: {key}."
            error(error_message)
            raise ValueError(error_message)
