from configparser import SectionProxy
from http.client import HTTPConnection, HTTPResponse
from logging import error


def get_connection(server_data: SectionProxy) -> HTTPConnection:
    """Gets the connection to the server.

    Args:
        server_data (SectionProxy): The server data.

    Returns:
        HTTPSConnection: The connection to the server.
    """

    host = server_data["host"]
    port = int(server_data["port"])
    timeout = int(server_data["timeout"])

    connection = HTTPConnection(host, port, timeout=timeout)
    return connection


def validate_endpoint(endpoint: str) -> str:
    """Validates and formats a endpoint.

    Checks if the endpoint is empty and a string and formats it by
    removing any trailing slashes.

    Args:
        endpoint (str): The endpoint to validate and format.

    Returns:
        str: The formatted endpoint.

    Raises:
        ValueError: If the endpoint is empty.
        TypeError: If the endpoint is not a string.
    """

    if not endpoint:
        raise ValueError("Endpoint cannot be empty.")

    if not isinstance(endpoint, str):
        raise TypeError("Endpoint must be a string.")

    splitted_endpoint = endpoint.split("/")
    formatted_endpoint = (
        "/" + "/".join([part for part in splitted_endpoint if part]) + "/"
    )

    return formatted_endpoint


def decode_response(response: HTTPResponse) -> str:
    """Decodes a response.

    Checks if the response is empty and an instance of HTTPResponse
    and decodes it.

    Args:
        response (HTTPResponse): The response to decode.

    Returns:
        str: The decoded response.

    Raises:
        ValueError: If the response is empty.
        TypeError: If the response is not a HTTPResponse.
    """

    if not response:
        raise ValueError("Response cannot be empty.")

    if not isinstance(response, HTTPResponse):
        raise TypeError("Response must be an instance of http.client.HTTPResponse.")

    return response.read().decode()
