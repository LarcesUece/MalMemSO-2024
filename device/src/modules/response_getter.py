from http.server import BaseHTTPRequestHandler, HTTPServer
from json import loads
from logging import error, info

from utils import get_connection, get_token, validate_endpoint


def get_response(filename, server_data, endpoint_data):
    connection = get_connection(server_data)
    token = get_token(connection, server_data, endpoint_data)

    response_endpoint = validate_endpoint(endpoint_data["response"])
    headers = {"Authorization": f"Bearer {token}"}

    connection.request("GET", url=response_endpoint, headers=headers)
    response = connection.getresponse()

    if response != filename:
        return None

    return response
