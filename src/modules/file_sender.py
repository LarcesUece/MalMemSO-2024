"""
Module for sending files to a remote service.

Functions:
    send_file(filepath: str) -> str: Sends a file to a remote service.
"""

from http.client import HTTPException
from logging import error, info
from os.path import basename
from uuid import uuid4

from ..config.config import ENDPOINT_DATA
from ..utils.client import get_connection, validate_endpoint


def send_file(filepath: str) -> str:
    """Sends a file to a remote service.

    Args:
        filepath (str): Path to the file to send.

    Returns:
        str: The name of the uploaded file.

    Raises:
        HTTPException: If the upload fails.
        ConnectionError: If a connection error occurs.
    """

    endpoint_data = ENDPOINT_DATA

    info("Starting file upload to service.")

    connection = get_connection()
    upload_endpoint = validate_endpoint(endpoint_data["upload"])
    filename = basename(filepath)

    boundary = str(uuid4())
    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }

    try:
        with open(filepath, "rb") as file:
            file_data = file.read()

            body = (
                (
                    f"--{boundary}\r\n"
                    f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
                    "Content-Type: application/octet-stream\r\n\r\n"
                ).encode()
                + file_data
                + f"\r\n--{boundary}--\r\n".encode()
            )

            connection.request("POST", url=upload_endpoint, body=body, headers=headers)
            response = connection.getresponse()

            if response.status not in [200, 201]:
                raise HTTPException(
                    f"Failed to upload file. Status: {response.status}."
                )
    except ConnectionError as exc:
        error_message = "An connection error occurred while uploading file."
        error(error_message)
        raise ConnectionError(error_message) from exc

    info("File upload complete.")

    return filename
