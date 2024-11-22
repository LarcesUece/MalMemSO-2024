from argparse import ArgumentParser
from logging import basicConfig, INFO
from os import pardir
from os.path import dirname, realpath, abspath, join

from dump_extractor import (
    extract_dump,
    TOOL_DEFAULT,
    TOOL_OPTIONS,
    ARCH_DEFAULT,
    ARCH_OPTIONS,
)

CURRENT_PATH = dirname(realpath(__file__))
LOGS_PATH = abspath(join(CURRENT_PATH, pardir, "logs"))
RAW_PATH = abspath(join(CURRENT_PATH, pardir, "dumps", "raw"))

if __name__ == "__main__":
    basicConfig(
        filename="logs/main.log",
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

    extract_dump(args.tool, args.arch)
