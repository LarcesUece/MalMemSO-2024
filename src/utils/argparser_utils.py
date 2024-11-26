from argparse import ArgumentParser
from inspect import stack
from logging import error
from os.path import basename, splitext

from utils.options import (
    DUMP_EXTRACTOR_ARCH_OPTIONS,
    DUMP_EXTRACTOR_TOOL_OPTIONS,
    DUMP_EXTRACTOR_TOOL_DEFAULT,
    DUMP_EXTRACTOR_ARCH_DEFAULT,
)

PARSER_DESCRIPTION = {
    "app": "Detect malware using AI through memory dump files",
    "dump_cleaner": "Clean the dump files directory",
    "dump_extractor": "Run a tool to extract a dump file",
    "file_compressor": "Compress a raw dump file",
    "file_sender": "Send a compressed dump file to the server",
    "malware_remover": "Remove a malware from the system",
    "network_disabler": "Disable all the network interfaces",
    "network_enabler": "Enable all the network interfaces",
}

PARSER_ARGS = {
    "app": {
        ("-t", "--tool"): {
            "type": str,
            "choices": DUMP_EXTRACTOR_TOOL_OPTIONS,
            "default": DUMP_EXTRACTOR_TOOL_DEFAULT,
            "help": "Memory dump tool to use",
        },
        ("-a", "--arch"): {
            "type": str,
            "choices": DUMP_EXTRACTOR_ARCH_OPTIONS,
            "default": DUMP_EXTRACTOR_ARCH_DEFAULT,
            "help": "Architecture of the system",
        },
    },
    "dump_cleaner": {},
    "dump_extractor": {
        ("-t", "--tool"): {
            "type": str,
            "choices": DUMP_EXTRACTOR_TOOL_OPTIONS,
            "default": DUMP_EXTRACTOR_TOOL_DEFAULT,
            "help": "Memory dump tool to use",
        },
        ("-a", "--arch"): {
            "type": str,
            "choices": DUMP_EXTRACTOR_ARCH_OPTIONS,
            "default": DUMP_EXTRACTOR_ARCH_DEFAULT,
            "help": "Architecture of the system",
        },
    },
    "file_compressor": {},
    "file_sender": {"file_path": {"type": str, "help": "Path to the file to be sent"}},
    "malware_remover": {},
    "network_disabler": {},
    "network_enabler": {},
}


def setup_argparser():
    """Setup the argument parser for the given module."""

    caller_file = stack()[1].filename
    module_name = _get_module_name(caller_file)

    if module_name not in PARSER_DESCRIPTION or module_name not in PARSER_ARGS:
        error_message = (
            f"Missing parser description or arguments for module: {module_name}"
        )
        error(error_message)
        raise ValueError(error_message)

    parser_description = PARSER_DESCRIPTION[module_name]
    parser = ArgumentParser(description=parser_description)
    for arg_name, arg_data in PARSER_ARGS[module_name].items():
        if isinstance(arg_name, tuple):
            parser.add_argument(*arg_name, **arg_data)
        else:
            parser.add_argument(arg_name, **arg_data)
    args = parser.parse_args()
    return args


def _get_module_name(caller_file=None):
    """Get the name of the module that called the function."""

    if not caller_file:
        error_message = "Caller file not provided"
        error(error_message)
        raise ValueError(error_message)

    module_name = splitext(basename(caller_file))[0]
    return module_name
