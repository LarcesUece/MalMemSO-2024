from argparse import ArgumentParser
from logging import basicConfig, info, error, INFO
from os import pardir, listdir, remove
from os.path import dirname, realpath, abspath, join, exists
from subprocess import Popen, PIPE, CalledProcessError

# PATHS
CURRENT_PATH = dirname(realpath(__file__))
X64_PATH = abspath(join(CURRENT_PATH, pardir, "bin", "x64"))
X86_PATH = abspath(join(CURRENT_PATH, pardir, "bin", "x86"))
LOGS_PATH = abspath(join(CURRENT_PATH, pardir, "logs"))
RAW_PATH = abspath(join(CURRENT_PATH, pardir, "dumps", "raw"))

# OPTIONS
TOOL_OPTIONS = ["winpmem", "dumpit"]
TOOL_DEFAULT = "winpmem"
ARCH_OPTIONS = ["x64", "x86"]
ARCH_DEFAULT = "x64"


def _get_command(tool, tool_path, output_path):
    """Get the command to execute the memory dump tool."""

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

    files = listdir(RAW_PATH)
    files = [f for f in files if f.startswith(f"dump_{tool}_{arch}")]
    numbers = [int(f.split("_")[-1].split(".")[0]) for f in files]
    number = max(numbers) + 1 if numbers else 1

    return join(RAW_PATH, f"dump_{tool}_{arch}_{number}.raw")


def _delete_corrupted_file(file_path):
    """Delete a corrupted file if it exists."""

    if exists(file_path):
        info(f"Deleting corrupted file {file_path}")
        remove(file_path)
    else:
        error(f"File {file_path} not found")


def extract_dump(tool=TOOL_DEFAULT, arch=ARCH_DEFAULT):
    """Run the memory dump tool."""

    info(f"Extracting memory dump using {tool.capitalize()} tool")

    arch_path = X64_PATH if arch == "x64" else X86_PATH
    tool_path = join(arch_path, f"{tool}.exe")
    output_path = _get_output_path(tool, arch)
    command = _get_command(tool, tool_path, output_path)

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
        process.terminate()


if __name__ == "__main__":
    """Log file and argument parser configuration."""

    basicConfig(
        filename=join(LOGS_PATH, "dump_extractor.log"),
        level=INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    parser = ArgumentParser(
        prog="dump_extractor.py",
        description="Extract a memory dump file to the dumps/raw folder",
    )
    parser.add_argument(
        "-t",
        "--tool",
        type=str,
        default=TOOL_DEFAULT,
        help="Tool used to extract memory dump file",
        choices=TOOL_OPTIONS,
    )
    parser.add_argument(
        "-a",
        "--arch",
        type=str,
        default=ARCH_DEFAULT,
        help="Architecture of the target system",
        choices=ARCH_OPTIONS,
    )
    args = parser.parse_args()

    extract_dump(args.tool, args.arch)
