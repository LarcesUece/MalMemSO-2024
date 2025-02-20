import ctypes
from logging import error, info
from os import makedirs, remove
from os.path import exists
from platform import architecture, release, system


def get_os() -> str:
    """Get the operating system of the current system."""

    os_name = system()
    if os_name == "Darwin":
        return "macos"
    if os_name in ["Windows", "Linux"]:
        return os_name.lower()

    error_message = f"Unsupported OS: {os_name}"
    error(error_message)
    raise ValueError(error_message)


def get_arch() -> str:
    """Get the architecture of the current system."""

    arch = architecture()[0]
    if arch in ["32bit", "64bit"]:
        return arch

    error_message = f"Unsupported architecture: {arch}"
    error(error_message)
    raise ValueError(error_message)


def is_root() -> bool:
    """Check if the current user is root/administrator."""

    os_name = get_os()

    if os_name == "windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    elif os_name == "linux":
        from os import getuid

        return getuid() == 0

    error_message = f"Unsupported OS: {os_name}"
    error(error_message)
    raise ValueError(error_message)


def create_dir(path: str) -> None:
    """Create a directory at the given path."""

    if not exists(path):
        try:
            makedirs(path)
        except PermissionError as exc:
            error_message = f"Failed to create directory at {path}."
            error(error_message)
            raise PermissionError(error_message) from exc


def delete_file_if_exists(filepath: str) -> None:
    if exists(filepath):
        try:
            remove(filepath)
            info(f"Deleted file at {filepath}.")
        except PermissionError as exc:
            error_message = f"Failed to delete file at {filepath}."
            error(error_message)
            raise PermissionError(error_message) from exc


def check_supported_os() -> None:
    os_name = system()
    os_release = release()

    if not os_name == "Windows" and not os_release == "10":
        error_message = (
            f"Unsupported OS: {os_name} {os_release}. This program requires Windows 10."
        )
        error(error_message)
        raise EnvironmentError(error_message)
