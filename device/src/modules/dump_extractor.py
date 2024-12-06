from logging import info, error
from os import listdir, stat
from os.path import join, exists
from subprocess import Popen, PIPE, CalledProcessError

from utils import BIN_PATH, RAW_PATH, create_dir, delete_file


def extract_dump(tool=None, arch=None):
    """Run the memory dump tool."""

    formatted_arch = _validate_extract_dump_args(tool, arch)

    info(f"Extracting memory dump using {tool.capitalize()} tool.")

    tool_path = join(BIN_PATH, f"{tool}_{formatted_arch}.exe")
    output_path = _get_output_path(tool, formatted_arch)
    command = _get_tool_command(tool, tool_path, output_path)

    info(f"Running command: {command}.")
    extraction_error = False

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

    info(f"Output message: {stdout}")
    info(f"Memory dump file saved at {output_path}.")

    return output_path


def _get_tool_command(tool, tool_path, output_path):
    """Get the command to execute the memory dump tool."""

    info(f"Getting command for {tool.capitalize()} tool")

    COMMANDS = {
        "winpmem": [tool_path, output_path],
        "dumpit": [tool_path, "/OUTPUT", output_path, "/Q"],
    }

    if tool not in COMMANDS:
        error_message = f"Tool not supported: {tool}."
        error(error_message)
        raise ValueError(error_message)

    return COMMANDS[tool]


def _get_output_path(tool, arch):
    """Get the output path for the memory dump file.

    The format of the output path is dump_<tool>_<arch>_<number>.raw.
    - tool: Tool used to extract the memory dump file.
    - arch: Architecture of the target system.
    - number: Next available number for the memory dump file.
    """

    if not exists(RAW_PATH):
        try:
            create_dir(RAW_PATH)
        except:
            error_message = "Failed to create raw output directory."
            error(error_message)
            raise PermissionError(error_message)

    info("Getting output path for memory dump file")

    files = listdir(RAW_PATH)
    files = [f for f in files if f.startswith(f"dump_{tool}_{arch}_")]
    numbers = [int(f.split("_")[-1].split(".")[0]) for f in files]
    number = max(numbers) + 1 if numbers else 1

    return join(RAW_PATH, f"dump_{tool}_{arch}_{number}.raw")


def _is_dump_empty(filepath):
    """Check if the dump file is empty."""

    if exists(filepath):
        file_size = stat(filepath).st_size
        return not file_size

    return True


def _validate_extract_dump_args(tool, arch):
    """Validate the arguments for the extract_dump function."""

    if not tool or not arch:
        error_message = "Tool and architecture must be provided."
        error(error_message)
        raise ValueError(error_message)

    if not isinstance(tool, str) or not isinstance(arch, str):
        error_message = "Tool and architecture must be strings."
        error(error_message)
        raise ValueError(error_message)

    if arch == "32bit":
        formatted_arch = "x86"
    elif arch == "64bit":
        formatted_arch = "x64"
    else:
        error_message = f"Architecture not supported: {arch}."
        error(error_message)
        raise ValueError(error_message)

    return formatted_arch
