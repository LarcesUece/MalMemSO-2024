from logging import info, error, warning
from os import listdir, remove, stat
from os.path import join, exists
from subprocess import Popen, PIPE, CalledProcessError

from utils import (
    DUMP_EXTRACTOR_TOOL_DEFAULT,
    DUMP_EXTRACTOR_ARCH_DEFAULT,
    X64_PATH,
    X86_PATH,
    RAW_DUMPS_PATH,
)


def _get_command(tool, tool_path, output_path):
    """Get the command to execute the memory dump tool."""

    info(f"Getting command for {tool.capitalize()} tool")

    COMMANDS = {
        "winpmem": [tool_path, output_path],
        "dumpit": [tool_path, "/OUTPUT", output_path, "/Q"],
    }

    return COMMANDS[tool]


def _get_output_path(tool, arch):
    """Get the output path for the memory dump file.

    The format of the output path is dump_<tool>_<arch>_<number>.raw.
    - tool: Tool used to extract the memory dump file.
    - arch: Architecture of the target system.
    - number: Next available number for the memory dump file.
    """

    info("Getting output path for memory dump file")

    files = listdir(RAW_DUMPS_PATH)
    files = [f for f in files if f.startswith(f"dump_{tool}_{arch}")]
    numbers = [int(f.split("_")[-1].split(".")[0]) for f in files]
    number = max(numbers) + 1 if numbers else 1

    return join(RAW_DUMPS_PATH, f"dump_{tool}_{arch}_{number}.raw")


def _delete_file_if_empty(filepath):
    """Delete a file if it is empty."""

    info(f"Checking if file is empty")

    if exists(filepath):
        file_size = stat(filepath).st_size
        if not file_size:
            warning(f"Deleting empty file {filepath}")
            remove(filepath)


def _delete_corrupted_file(filepath):
    """Delete a corrupted file if it exists."""

    if exists(filepath):
        warning(f"Deleting corrupted file")
        remove(filepath)


def extract_dump(tool=DUMP_EXTRACTOR_TOOL_DEFAULT, arch=DUMP_EXTRACTOR_ARCH_DEFAULT):
    """Run the memory dump tool."""

    info(f"Extracting memory dump using {tool.capitalize()} tool")

    arch_path = X64_PATH if arch == "x64" else X86_PATH
    tool_path = join(arch_path, f"{tool}.exe")
    output_path = _get_output_path(tool, arch)
    command = _get_command(tool, tool_path, output_path)

    info(f"Running command: {command}")

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
        error(f"A subprocess error occurred: {e}")
        _delete_corrupted_file(output_path)
    except Exception as e:
        error(f"An unexpected error occurred: {e}")
        _delete_corrupted_file(output_path)
    else:
        if stderr:
            error(f"An error occurred: {stderr}")

        info(f"Output message: {stdout}")
        info(f"Memory dump file saved at {output_path}")
        _delete_file_if_empty(output_path)

        process.terminate()
