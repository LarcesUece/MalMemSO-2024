import ctypes

from logging import error
from os import makedirs, remove
from os.path import exists
from platform import system, architecture


def get_os():
    """Get the operating system of the current system."""

    os_name = system()
    if os_name == "Darwin":
        return "macos"
    if os_name in ["Windows", "Linux"]:
        return os_name.lower()

    error_message = f"Unsupported OS: {os_name}"
    error(error_message)
    raise ValueError(error_message)


def get_arch():
    """Get the architecture of the current system."""

    arch = architecture()[0]
    if arch in ["32bit", "64bit"]:
        return arch

    error_message = f"Unsupported architecture: {arch}"
    error(error_message)
    raise ValueError(error_message)


def is_root():
    """Check if the current user is root/administrator."""

    os_name = get_os()

    if os_name == "windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    elif os_name == "linux":
        from os import getuid

        return getuid() == 0

    error_message = f"Unsupported OS: {os_name}"
    error(error_message)
    raise ValueError(error_message)


def create_dir(path):
    """Create a directory at the given path."""

    if not exists(path):
        try:
            makedirs(path)
        except:
            error_message = f"Failed to create directory at {path}."
            error(error_message)
            raise PermissionError(error_message)


def delete_file(filepath):
    """Delete a file if it exists."""

    if exists(filepath):
        try:
            remove(filepath)
        except:
            error_message = f"Failed to delete file at {filepath}."
            error(error_message)
            raise PermissionError(error_message)
