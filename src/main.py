from argparse import ArgumentParser
from logging import basicConfig, INFO, error, info
from os import makedirs
from os.path import abspath, join, isdir

from utils import COMPRESSED_PATH, RAW_PATH, LOGS_PATH, X64_PATH, X86_PATH
from dump_extractor import (
    extract_dump,
    TOOL_DEFAULT,
    TOOL_OPTIONS,
    ARCH_DEFAULT,
    ARCH_OPTIONS,
)

LOG_FILE_PATH = abspath(join(LOGS_PATH, "main.log"))


def _create_log_folder():
    """Create the folder for the log files."""

    if not isdir(LOGS_PATH):
        makedirs(LOGS_PATH)
        info(f"Created folder {LOGS_PATH}")


def _init_project():
    """Create necessary folders and check for required files."""

    info("Initializing project")

    if not isdir(X64_PATH) or not isdir(X86_PATH):
        error("Missing bin folder with memory dump tools executable files")
        raise SystemExit

    if not isdir(COMPRESSED_PATH):
        makedirs(COMPRESSED_PATH)
        info(f"Created folder {COMPRESSED_PATH}")

    if not isdir(RAW_PATH):
        makedirs(RAW_PATH)
        info(f"Created folder {RAW_PATH}")

    info("All folders are ready")


if __name__ == "__main__":
    """Initialize the project and call all the program functions."""

    _create_log_folder()

    basicConfig(
        filename=LOG_FILE_PATH,
        level=INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    parser = ArgumentParser(
        prog="main.py",
        description="Detect malware using AI through memory dump files",
    )
    parser.add_argument(
        "-t",
        "--tool",
        choices=TOOL_OPTIONS,
        default=TOOL_DEFAULT,
        help="Tool used to extract memory dump file",
    )
    parser.add_argument(
        "-a",
        "--arch",
        choices=ARCH_OPTIONS,
        default=ARCH_DEFAULT,
        help="Architecture of the target system",
    )
    args = parser.parse_args()

    _init_project()
    extract_dump(args.tool, args.arch)
