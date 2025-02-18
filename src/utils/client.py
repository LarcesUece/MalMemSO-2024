from configparser import SectionProxy
from http.client import HTTPResponse, HTTPSConnection
from json import dumps, loads
from logging import error
from ssl import create_default_context


def get_connection(server_data: SectionProxy) -> HTTPSConnection:
    """Gets the connection to the server.

    Args:
        server_data (SectionProxy): The server data.

    Returns:
        HTTPSConnection: The connection to the server.
    """

    host = server_data["host"]
    port = int(server_data["port"])
    timeout = server_data["timeout"]
    context = create_default_context()

    connection = HTTPSConnection(host, port, timeout=timeout, context=context)
    return connection


def get_token(
    connection: HTTPSConnection, server_data: SectionProxy, endpoint_data: SectionProxy
) -> str:
    """Gets the access token from the server.

    Args:
        connection (HTTPSConnection): The connection to the server.
        server_data (SectionProxy): The server data.
        endpoint_data (SectionProxy): The endpoint data.

    Returns:
        str: The access token.

    Raises:
        Exception: If it fails to get the access token.
    """

    username = server_data["username"]
    password = server_data["password"]
    data = dumps({"username": username, "password": password})

    headers = {"Content-Type": "application/json"}
    login_endpoint = validate_endpoint(endpoint_data["login"])

    try:
        connection.request("POST", url=login_endpoint, body=data, headers=headers)
        response = connection.getresponse()
        token = loads(decode_response(response))["access_token"]
    except Exception as exc:
        error_message = "Failed to get access token."
        error(error_message)
        raise RuntimeError(error_message) from exc

    return token


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
    formatted_endpoint = "/" + "/".join([part for part in splitted_endpoint if part])

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
