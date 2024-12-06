from http.client import HTTPConnection, HTTPException
from os.path import basename
from logging import error


def upload_file(filepath, server_data):
    host = server_data["host"]
    port = int(server_data["port"])
    username = server_data["username"]
    password = server_data["password"]
    endpoint = server_data["endpoint"]
    timeout = server_data["timeout"]

    try:
        conn = HTTPConnection(host, port, timeout)
        with open(filepath, "rb") as file:
            file_data = file.read()
            headers = {
                "Content-Length": str(len(file_data)),
                "Filename": basename(filepath),
            }
        conn.request("POST", url=endpoint, body=file_data, headers=headers)
        response = conn.getresponse()
    except HTTPException as e:
        error_message = "Failed to upload file."
        error(error_message, exc_info=True)
        raise e(error_message)
    except OSError as e:
        error_message = "Failed to access file."
        error(error_message, exc_info=True)
        raise e(error_message)
    except Exception as e:
        error_message = "An error occurred."
        error(error_message, exc_info=True)
        raise e(error_message)
    else:
        conn.close()
        return response.read().decode()
