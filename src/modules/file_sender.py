from configparser import SectionProxy
from http.client import HTTPException
from logging import error, info
from os.path import basename

from utils import get_connection, get_token, validate_endpoint


def send_file(
    filepath: str, server_data: SectionProxy, endpoint_data: SectionProxy
) -> str:
    connection = get_connection(server_data)
    # token = get_token(connection, server_data, endpoint_data)

    upload_endpoint = validate_endpoint(endpoint_data["upload"])
    filename = basename(filepath)

    headers = {
        # "Authorization": f"Bearer {token}",
        "Content-Type": "multipart/form-data",
        "Filename": filename,
    }

    try:
        with open(filepath, "rb") as file:
            connection.request("POST", url=upload_endpoint, body=file, headers=headers)
            response = connection.getresponse()

            if response.status != 200:
                raise HTTPException(
                    f"Failed to upload file. Status: {response.status}."
                )
    except OSError as e:
        error_message = "Failed to access file."
        error(error_message)
        raise e(error_message)
    except Exception as e:
        error_message = "An error occurred."
        error(error_message)
        raise e(error_message)

    return filename
