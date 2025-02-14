from logging import info, error
from os import listdir, stat
from os.path import join, exists
from subprocess import Popen, PIPE, CalledProcessError

from utils import BIN_PATH, RAW_PATH, create_dir, delete_file


def extract_dump(tool: str, arch: str) -> str:
    """Extracts the memory dump file using the specified tool and
    architecture.

    Validates the tool and architecture provided, gets the path to the
    tool executable, creates the output path for the memory dump file,
    and executes the tool command. If an error occurs during memory
    dump extraction, the output file is deleted.

    Args:
        tool (str): Tool used to extract the memory dump file.
        arch (str): Architecture of the target system.

    Returns:
        str: Path to the memory dump file.

    Raises:
        ValueError: If the tool or architecture is not provided or
        invalid.
        PermissionError: If the raw output directory cannot be created.
        Exception: If an error occurs during memory dump extraction.
    """

    info("Running memory dump extraction.")

    formatted_arch = _validate_extract_dump_args(tool, arch)
    tool_path = join(BIN_PATH, f"{tool}_{formatted_arch}.exe")
    output_path = _get_output_path(tool, formatted_arch)
    command = _get_tool_command(tool, tool_path, output_path)
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
            error(error_message)
            extraction_error = True
        process.terminate()

    if extraction_error:
        delete_file(output_path)
        raise Exception(error_message)

    info(f"Output message: {stdout}.")
    info(f"Memory dump file saved at {output_path}.")

    return output_path


def _validate_extract_dump_args(tool: str, arch: str) -> str:
    """Validates the arguments for the extract_dump function.

    Checks if the tool and architecture are provided and valid. The
    architecture is formatted as "x86" or "x64" based on the provided
    architecture. Returns the formatted architecture.

    Args:
        tool (str): Tool used to extract the memory dump file.
        arch (str): Architecture of the target system.

    Returns:
        str: Formatted architecture.

    Raises:
        ValueError: If the tool or architecture is not provided or
        invalid.
    """

    info("Validating tool and arch provided for memory dump extraction.")

    if not tool or not arch:
        error_message = "Tool and architecture must be provided."
        error(error_message)
        raise ValueError(error_message)

    if not isinstance(tool, str) or not isinstance(arch, str):
        error_message = "Tool and architecture must be strings."
        error(error_message)
        raise ValueError(error_message)

    info("Tool is valid.")

    if arch == "32bit":
        formatted_arch = "x86"
    elif arch == "64bit":
        formatted_arch = "x64"
    else:
        error_message = f"Architecture not supported: {arch}."
        error(error_message)
        raise ValueError(error_message)

    info("Arch is valid.")

    return formatted_arch


def _get_output_path(tool: str, arch: str) -> str:
    """Gets the output path for the memory dump file.

    Creates the raw output directory if it does not exist, gets the
    next available number for the memory dump file, and returns the
    output path. The output path is formatted as
    "dump_<tool>_<arch>_<number>.raw". The number is incremented by 1
    for each memory dump file existing in the directory.

    Args:
        tool (str): Tool used to extract the memory dump file.
        arch (str): Architecture of the target system.

    Returns:
        str: Path to the memory dump file.

    Raises:
        PermissionError: If the raw output directory cannot be created.
    """

    if not exists(RAW_PATH):
        try:
            create_dir(RAW_PATH)
            info("Raw output directory created.")
        except:
            error_message = "Failed to create raw output directory."
            error(error_message)
            raise PermissionError(error_message)

    info("Getting output path for memory dump file.")

    files = listdir(RAW_PATH)
    files = [f for f in files if f.startswith(f"dump_{tool}_{arch}_")]
    numbers = [int(f.split("_")[-1].split(".")[0]) for f in files]
    number = max(numbers) + 1 if numbers else 1

    return join(RAW_PATH, f"dump_{tool}_{arch}_{number}.raw")


def _get_tool_command(tool: str, tool_path: str, output_path: str) -> list:
    """Gets the command to execute the memory dump tool.

    Checks if the tool is supported and returns the command to execute
    the tool.

    Args:
        tool (str): Tool used to extract the memory dump file.
        tool_path (str): Path to the tool executable.
        output_path (str): Path to the memory dump file.

    Returns:
        list: Command to execute the memory dump tool.

    Raises:
        ValueError: If the tool is not supported.

    Supported tools:
        WinPmem
        DumpIt for Windows
    """

    info(f"Getting command for {tool.capitalize()} tool.")

    COMMANDS = {
        "winpmem": [tool_path, output_path],
        "dumpit": [tool_path, "/OUTPUT", output_path, "/Q"],
    }

    if tool not in COMMANDS:
        error_message = f"Tool not supported: {tool}."
        error(error_message)
        raise ValueError(error_message)

    return COMMANDS[tool]


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
        file_size = stat(filepath).st_size
        return not file_size

    return True
