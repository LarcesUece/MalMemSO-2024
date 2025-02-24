"""
Utility module for HTTP client operations.

Functions:
    get_connection() -> http.client.HTTPConnection: Creates and returns 
        an HTTP connection.
    validate_endpoint(endpoint: str) -> str: Validates and formats an 
        endpoint.
    decode_response(response: http.client.HTTPResponse) -> str: Decodes 
        an HTTP response.
"""

from http.client import HTTPConnection, HTTPResponse
from logging import error, info

from ..config.config import SERVICE_DATA


def get_connection() -> HTTPConnection:
    """Creates and returns an HTTP connection using service data.

    Returns:
        http.client.HTTPConnection: The created HTTP connection.
    """

    host = SERVICE_DATA["host"]
    port = int(SERVICE_DATA["port"])
    timeout = int(SERVICE_DATA["timeout"])

    connection = HTTPConnection(host, port, timeout=timeout)

    info("Connection created.")

    return connection


def validate_endpoint(endpoint: str) -> str:
    """Validates and formats an endpoint.

    Args:
        endpoint (str): The endpoint to validate.

    Returns:
        str: The formatted endpoint.

    Raises:
        ValueError: If the endpoint is empty.
        TypeError: If the endpoint is not a string.
    """

    if not endpoint:
        error_message = "Endpoint cannot be empty."
        error(error_message)
        raise ValueError(error_message)

    if not isinstance(endpoint, str):
        error_message = "Endpoint must be a string."
        error(error_message)
        raise TypeError(error_message)

    splitted_endpoint = endpoint.split("/")
    formatted_endpoint = (
        "/" + "/".join([part for part in splitted_endpoint if part]) + "/"
    )

    info("Endpoint validated and formatted.")

    return formatted_endpoint


def decode_response(response: HTTPResponse) -> str:
    """Decodes an HTTP response.

    Args:
        response (http.client.HTTPResponse): The HTTP response to
            decode.

    Returns:
        str: The decoded response content.

    Raises:
        ValueError: If the response is empty.
        TypeError: If the response is not an HTTPResponse instance.
    """

    if not response:
        error_message = "Response cannot be empty."
        error(error_message)
        raise ValueError(error_message)

    if not isinstance(response, HTTPResponse):
        error_message = "Response must be an instance of http.client.HTTPResponse."
        error(error_message)
        raise TypeError(error_message)

    return response.read().decode()
