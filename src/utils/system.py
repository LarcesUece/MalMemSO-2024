"""
Utility module for system-related operations.

Functions:
    delete_file_if_exists(filepath: str) -> None: Deletes a file if it 
        exists.
    check_supported_os() -> None: Checks if the OS is supported.
"""

from logging import error, info
from os import remove
from os.path import exists
from platform import release, system


def delete_file_if_exists(filepath: str) -> None:
    """Deletes a file if it exists.

    Args:
        filepath (str): Path to the file to delete.

    Raises:
        PermissionError: If deletion fails due to permission issues.
    """

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
    """Checks if the OS is Windows 10.

    Raises:
        EnvironmentError: If the OS is not supported.
    """

    os_name = system()
    os_release = release()

    if not os_name == "Windows" and not os_release == "10":
        error_message = (
            f"Unsupported OS: {os_name} {os_release}. This program requires Windows 10."
        )
        error(error_message)
        raise EnvironmentError(error_message)

    info("Operating system is supported.")
