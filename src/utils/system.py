"""
System Utilities

This module provides utility functions to interact with and manage the
current system environment, including checking the operating system and 
deleting files.

Functions:
    - delete_file_if_exists(filepath): Deletes the specified file if it
        exists.
    - check_supported_os(): Verifies if the current OS is Windows 10.
"""

from logging import error, info
from os import remove
from os.path import exists
from platform import release, system


def delete_file_if_exists(filepath: str) -> None:
    if exists(filepath):
        try:
            remove(filepath)
            info(f"Deleted file at {filepath}.")
        except PermissionError as exc:
            error_message = f"Failed to delete file at {filepath}."
            error(error_message)
            raise PermissionError(error_message) from exc

    info(f"File at {filepath} does not exist.")


def check_supported_os() -> None:
    os_name = system()
    os_release = release()

    if not os_name == "Windows" and not os_release == "10":
        error_message = (
            f"Unsupported OS: {os_name} {os_release}. This program requires Windows 10."
        )
        error(error_message)
        raise EnvironmentError(error_message)

    info("Operating system is supported.")
