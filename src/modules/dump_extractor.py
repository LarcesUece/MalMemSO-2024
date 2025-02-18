from logging import info, error
from os import listdir, stat
from os.path import join, exists, getsize
from subprocess import Popen, PIPE, CalledProcessError

from ..config import (
    BIN_DIR,
    RAW_DIR,
    PARSER_ARCH_OPTIONS,
    PARSER_ARCH_MAPPING,
    PARSER_ARCH_DEFAULT,
    PARSER_TOOL_OPTIONS,
    PARSER_TOOL_DEFAULT,
    TOOL_COMMANDS,
)
from ..utils import delete_file_if_exists


def extract_dump(
    tool: str = PARSER_TOOL_DEFAULT, arch: str = PARSER_ARCH_DEFAULT
) -> str:
    """Extracts the memory dump file using the specified tool and
    architecture.

    Validates the values provided and generates the required paths to
    execute the tool command. If an error occurs during memory dump
    extraction, the output file is deleted. If no tool or architecture
    is provided, the default values are used.

    Args:
        tool (str): Tool used to extract the memory dump file.
        arch (str): Architecture of the target system.

    Returns:
        str: Path to the memory dump file.

    Raises:
        Exception: If an error occurs during memory dump extraction.
    """

    info("Running memory dump extraction.")

    _validate_extract_dump_args(tool, arch)
    formatted_arch = PARSER_ARCH_MAPPING[arch]
    tool_path = join(BIN_DIR, f"{tool}_{formatted_arch}.exe")
    output_path = _generate_output_path(tool, formatted_arch)
    command = TOOL_COMMANDS[tool](tool_path, output_path)
    extraction_error = False

    info(f"Extracting memory dump using {tool.capitalize()} tool.")

    try:
        process = Popen(
            command,
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            encoding="utf-8",
        )
        stdout, stderr = process.communicate()
    except CalledProcessError as e:
        error_message = f"A subprocess error occurred: {e}."
        error(error_message)
        extraction_error = True
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}."
        error(error_message)
        extraction_error = True
    else:
        if stderr or _is_dump_empty(output_path) or (not stderr and not stdout):
            error_message = "An error occurred during memory dump extraction."
            if stderr:
                error_message += f" Error message: {stderr}."
            error(error_message)
            extraction_error = True
    finally:
        process.terminate()

    if extraction_error:
        delete_file_if_exists(output_path)
        raise Exception(error_message)

    info(f"Output message: {stdout}.")
    info(f"Memory dump file saved at {output_path}.")

    return output_path


def _validate_extract_dump_args(tool: str, arch: str) -> None:
    """Validates the arguments for the extract_dump function.

    Checks if the tool and architecture are valid.

    Args:
        tool (str): Tool used to extract the memory dump file.
        arch (str): Architecture of the target system.

    Raises:
        ValueError: If the tool or architecture is invalid.
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

    if tool not in PARSER_TOOL_OPTIONS:
        error_message = f"Tool not supported: {tool}."
        error(error_message)
        raise ValueError(error_message)

    info("Tool is valid.")

    if arch not in PARSER_ARCH_OPTIONS:
        error_message = f"Architecture not supported: {arch}."
        error(error_message)
        raise ValueError(error_message)

    info("Arch is valid.")


def _generate_output_path(tool: str, arch: str) -> str:
    """Generates the output path for the memory dump file.

    The output path is formatted as "dump_<tool>_<arch>_<number>.raw".
    This function gets the next available number for the memory dump
    file, and returns the output path.

    Args:
        tool (str): Tool used to extract the memory dump file.
        arch (str): Architecture of the target system.

    Returns:
        str: The path generated for the memory dump file.

    Raises:
        FileNotFoundError: If the raw output directory does not exist.
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
    """Checks if the dump file is empty.

    Checks if the memory dump file exists and has a size greater than
    0. Returns True if the file does not exist or is empty, False
    otherwise.

    Args:
        filepath (str): Path to the memory dump file.

    Returns:
        bool: True if the file is empty or does not exist, False
        otherwise.
    """

    if exists(filepath):
        file_size = getsize(filepath)
        return not file_size

    return True
