"""
Module for extracting memory dumps using specified tools and 
architectures.

Functions:
    extract_dump(tool: str, arch: str) -> str: Extracts a memory dump 
        using the specified tool and architecture.
"""

from logging import error, info
from os import listdir
from os.path import exists, getsize, join
from re import MULTILINE
from re import compile as re_compile
from subprocess import PIPE, Popen, SubprocessError

from ..config.config import (
    PARSER_ARCH_DEFAULT,
    PARSER_ARCH_MAPPING,
    PARSER_ARCH_OPTIONS,
    PARSER_TOOL_DEFAULT,
    PARSER_TOOL_OPTIONS,
    TOOL_COMMANDS,
)
from ..config.paths import BIN_DIR, RAW_DIR
from ..utils.system import delete_file_if_exists


def extract_dump(
    tool: str = PARSER_TOOL_DEFAULT, arch: str = PARSER_ARCH_DEFAULT
) -> str:
    """Extracts a memory dump using the specified tool and architecture.

    Args:
        tool (str): The tool to use for extraction.
        arch (str): The architecture to use.

    Returns:
        str: Path to the extracted memory dump file.

    Raises:
        SubprocessError: If an error occurs during extraction.
        RuntimeError: If the extraction fails.
    """

    info("Running memory dump extraction.")

    _validate_extract_dump_args(tool, arch)
    formatted_arch = PARSER_ARCH_MAPPING[arch]
    tool_path = join(BIN_DIR, f"{tool}_{formatted_arch}.exe")
    output_path = _generate_output_path(tool, formatted_arch)
    command = TOOL_COMMANDS.get(tool)(tool_path, output_path)
    # command = TOOL_COMMANDS[tool](tool_path, output_path)
    error_message = None

    info(f"Extracting memory dump using '{tool.capitalize()}' tool.")

    try:
        with Popen(command, stdout=PIPE, stderr=PIPE, text=True) as process:
            stdout, stderr = process.communicate()
    except SubprocessError as exc:
        error_message = f"Error occurred during memory dump extraction: {exc}."
        error(error_message)
        raise SubprocessError(error_message) from exc

    if stderr:
        error_message = stderr
    elif _is_dump_empty(output_path):
        error_message = "Memory dump file is empty."
    elif not stderr and not stdout:
        error_message = "No output message received from memory dump extraction."
    elif not _is_successful_stdout(stdout, tool):
        error_message = _extract_error_message(stdout, tool)
        if error_message is None:
            error_message = "Memory dump extraction was not successful."

    if error_message:
        error(error_message)
        error("Stdout: %s", stdout)
        error("Stderr: %s", stderr)
        delete_file_if_exists(output_path)
        raise RuntimeError(error_message)

    info(f"Output message: {stdout}.")
    info(f"Memory dump file saved at '{output_path}'.")

    return output_path


def _validate_extract_dump_args(tool: str, arch: str) -> None:
    """Validates the tool and architecture arguments.

    Args:
        tool (str): The tool to validate.
        arch (str): The architecture to validate.

    Raises:
        ValueError: If tool or architecture is invalid.
    """

    info("Validating tool and arch provided for memory dump extraction.")

    if not tool or not arch:
        error_message = "Tool and architecture cannot be empty."
        error(error_message)
        raise ValueError(error_message)

    if not isinstance(tool, str) or not isinstance(arch, str):
        error_message = "Tool and architecture must be strings."
        error(error_message)
        raise ValueError(error_message)

    if not tool in PARSER_TOOL_OPTIONS:
        error_message = f"Tool not supported: {tool}."
        error(error_message)
        raise ValueError(error_message)

    if not tool in TOOL_COMMANDS:
        error_message = f"Tool command not found: {tool}."
        error(error_message)
        raise ValueError(error_message)

    info("Tool is valid.")

    if not arch in PARSER_ARCH_OPTIONS:
        error_message = f"Architecture not supported: {arch}."
        error(error_message)
        raise ValueError(error_message)

    info("Arch is valid.")


def _generate_output_path(tool: str, arch: str) -> str:
    """Generates the output path for the extracted dump.

    Args:
        tool (str): The tool used.
        arch (str): The architecture used.

    Returns:
        str: The generated output path.
    """

    if not exists(RAW_DIR):
        error_message = "Raw output directory does not exist."
        error(error_message)
        raise FileNotFoundError(error_message)

    info("Generating output path for memory dump file.")

    files = listdir(RAW_DIR)
    files = [file for file in files if file.startswith(f"dump_{tool}_{arch}_")]
    numbers = [int(file.split("_")[-1].split(".")[0]) for file in files]
    next_number = max(numbers) + 1 if numbers else 1

    return join(RAW_DIR, f"dump_{tool}_{arch}_{next_number}.raw")


def _is_dump_empty(filepath: str) -> bool:
    """Checks if the extracted dump file is empty.

    Args:
        filepath (str): Path to the dump file.

    Returns:
        bool: True if the file is empty, False otherwise.
    """

    if exists(filepath):
        file_size = getsize(filepath)
        return not file_size

    return True


def _extract_error_message(stdout: str, tool: str) -> str | None:
    """Extracts an error message from stdout if extraction failed.

    Args:
        stdout (str): The standard output from the extraction.
        tool (str): The tool used for extraction.

    Returns:
        str | None: Extracted error message or None if not found.
    """

    if not tool in PARSER_TOOL_OPTIONS:
        return None

    error_patterns = {
        "dumpit": re_compile(r"^(?:error|Error|ERROR):\s*(.+)", MULTILINE),
        "winpmem": re_compile(r"^[ \t]*(Failed.*)", MULTILINE),
    }
    pattern = error_patterns.get(tool)
    match = pattern.search(stdout) if pattern else None
    return match.group(1).strip() if match else None


def _is_successful_stdout(stdout: str, tool: str) -> bool:
    """Validates if the stdout indicates a successful extraction.

    Args:
        stdout (str): The standard output from the extraction.
        tool (str): The tool used for extraction.

    Returns:
        bool: True if extraction was successful, False otherwise.
    """

    if tool == "dumpit":
        pattern = re_compile(r"^[ \t]*Acquisition finished at:.*", MULTILINE)
        return bool(pattern.search(stdout))

    if tool == "winpmem":
        return not "Failed" in stdout

    return False
