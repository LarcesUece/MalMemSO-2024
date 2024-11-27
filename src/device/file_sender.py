from ftplib import FTP
from logging import error
from os.path import exists

from utils import setup_argparser, load_config, setup_logging


def send_file(filepath):
    """Send a file to a remote server using FTP."""

    if not exists(filepath):
        error_message = f"File not found at {filepath}"
        error(error_message)
        raise FileNotFoundError(error_message)

    try:
        config = load_config()
        server_config = config["server"]

        SERVER = server_config["server"]
        PORT = int(server_config["port"])
        USERNAME = server_config["username"]
        PASSWORD = server_config["password"]
        ENDPOINT = server_config["endpoint"]
    except Exception as e:
        error_message = "Failed to load server configuration"
        error(error_message, exc_info=True)
        raise e(error_message)

    try:
        ftp = FTP()
        ftp.connect(SERVER, PORT)
        ftp.login(USERNAME, PASSWORD)
        ftp.cwd(ENDPOINT)

        with open(filepath, "rb") as f:
            ftp.storbinary(f"STOR {filepath}", f)
    except Exception as e:
        error_message = "Failed to send file"
        error(error_message, exc_info=True)
        raise e(error_message)
    finally:
        try:
            ftp.quit()
        except Exception as e:
            error_message = "Failed to close FTP connection"
            error(error_message, exc_info=True)
            raise e(error_message)


if __name__ == "__main__":
    setup_logging(custom_filename=True)
    args = setup_argparser()
    send_file(**vars(args))
