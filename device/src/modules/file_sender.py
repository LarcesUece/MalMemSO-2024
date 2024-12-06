from logging import error
from os.path import basename, exists
from http.client import HTTPConnection, HTTPException


def send_file(filepath, server_data):
    endpoint = server_data["endpoint"]
    connection = _connect(server_data)
    file_data, headers = _get_request_data(filepath)
    connection.request("POST", url=endpoint, body=file_data, headers=headers)
    response = connection.getresponse()
    connection.close()
    return response.read().decode()


def _connect(server_data):
    host = server_data["host"]
    port = int(server_data["port"])
    timeout = server_data["timeout"]

    try:
        connection = HTTPConnection(host, port, timeout)
        connection.connect()
    except HTTPException as e:
        error_message = "Failed to connect to server."
        error(error_message, exc_info=True)
        raise e(error_message)
    except Exception as e:
        error_message = "An error occurred."
        error(error_message, exc_info=True)
        raise e(error_message)

    return connection


def _get_request_data(filepath):
    if not exists(filepath):
        error_message = "File does not exist."
        error(error_message)
        raise FileNotFoundError(error_message)

    try:
        with open(filepath, "rb") as file:
            file_data = file.read()
            headers = {
                "Content-Length": str(len(file_data)),
                "Filename": basename(filepath),
            }
    except OSError as e:
        error_message = "Failed to access file."
        error(error_message, exc_info=True)
        raise e(error_message)
    except Exception as e:
        error_message = "An error occurred."
        error(error_message, exc_info=True)
        raise e(error_message)

    return file_data, headers
