"""
HTTP Client Utilities

This module provides utility functions to handle HTTP client 
operations, including establishing a connection, validating and 
formatting endpoints and decoding HTTP responses.

Functions:
    - get_connection(): Establishes and returns an HTTP connection to 
        the server using the provided service data.
    - validate_endpoint(endpoint): Validates and formats the given 
        endpoint by ensuring it is a non-empty string and with all the 
        trailing slashes necessary.
    - decode_response(response): Decodes the provided HTTP response, 
        ensuring it is an instance of HTTPResponse and not empty.
"""

from http.client import HTTPConnection, HTTPResponse
from logging import error, info

from ..config.config import SERVICE_DATA


def get_connection() -> HTTPConnection:
    """Establishes and returns a connection to the server.

    Uses the server data (host, port, timeout) from the configuration to
    establish an HTTP connection.

    Returns:
        http.client.HTTPConnection: The connection to the server.
    """

    host = SERVICE_DATA["host"]
    port = int(SERVICE_DATA["port"])
    timeout = int(SERVICE_DATA["timeout"])

    connection = HTTPConnection(host, port, timeout=timeout)

    info("Connection created.")

    return connection


def validate_endpoint(endpoint: str) -> str:
    """Validates and formats the given endpoint.

    Ensures the endpoint is a non-empty string and formats it ensuring
    it has all the trailing slashes necessary.

    Args:
        endpoint (str): The endpoint to validate and format.

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
    """Decodes the HTTP response.

    Reads and decodes the response content.

    Args:
        response (http.client.HTTPResponse): The response to decode.

    Returns:
        str: The decoded response content.

    Raises:
        ValueError: If the response is empty.
        TypeError: If the response is not an instance of HTTPResponse.
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
