from configparser import SectionProxy
from http.client import CannotSendRequest, ResponseNotReady
from json import loads
from logging import error, info
from time import sleep

from ..utils import decode_response, get_connection, validate_endpoint


def get_response(
    filename: str, server_data: SectionProxy, endpoint_data: SectionProxy
) -> dict:
    retry_interval = 60
    connection = None
    token = None
    headers = None
    response = None

    response_endpoint = validate_endpoint(endpoint_data["response"])

    while not response:
        if not connection:
            connection = get_connection(server_data)
        if not token:
            token = get_token(connection, server_data, endpoint_data)
            headers = {"Authorization": f"Bearer {token}"}
        try:
            connection.request("GET", url=response_endpoint, headers=headers)
            response = connection.getresponse()

            if response.status == 200:
                response_data = decode_response(response)
                if response_data.get("filename") == filename:
                    return response_data
            elif response.status == 401:
                token = None
                headers = None
            else:
                error_message = f"Failed to get response. Status: {response.status}."
                error(error_message)
        except (ResponseNotReady, CannotSendRequest):
            error_message = "Failed to get response."
            error(error_message)
            connection = None
        except Exception as exc:
            error_message = "An error occurred while getting response."
            error(error_message)
            raise RuntimeError(error_message) from exc

        sleep(retry_interval)
