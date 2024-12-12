# from logging import error
# from os.path import basename, exists
# from http.client import HTTPConnection, HTTPException


# def send_file(filepath, server_data):
#     endpoint = server_data["endpoint"]
#     connection = _connect(server_data)
#     file_data, headers = _get_request_data(filepath)
#     connection.request("POST", url=endpoint, body=file_data, headers=headers)
#     response = connection.getresponse()
#     connection.close()
#     return response.read().decode()


# def _connect(server_data):
#     host = server_data["host"]
#     port = int(server_data["port"])
#     timeout = server_data["timeout"]

#     try:
#         connection = HTTPConnection(host, port, timeout)
#         connection.connect()
#     except HTTPException as e:
#         error_message = "Failed to connect to server."
#         error(error_message, exc_info=True)
#         raise e(error_message)
#     except Exception as e:
#         error_message = "An error occurred."
#         error(error_message, exc_info=True)
#         raise e(error_message)

#     return connection


# def _get_request_data(filepath):
#     if not exists(filepath):
#         error_message = "File does not exist."
#         error(error_message)
#         raise FileNotFoundError(error_message)

#     try:
#         with open(filepath, "rb") as file:
#             file_data = file.read()
#             headers = {
#                 "Content-Length": str(len(file_data)),
#                 "Filename": basename(filepath),
#             }
#     except OSError as e:
#         error_message = "Failed to access file."
#         error(error_message, exc_info=True)
#         raise e(error_message)
#     except Exception as e:
#         error_message = "An error occurred."
#         error(error_message, exc_info=True)
#         raise e(error_message)

#     return file_data, headers


from http.client import HTTPResponse, HTTPSConnection, HTTPException
from json import dumps, loads
from ssl import create_default_context


def send_file(filepath, server_data):
    connection = _get_connection(server_data)
    token = _get_token(connection, server_data)

    upload_endpoint = _validate_endpoint(server_data["upload_endpoint"])
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "multipart/form-data",
    }

    with open(filepath, "rb") as file:
        connection.request("POST", url=upload_endpoint, body=file, headers=headers)
        response = connection.getresponse()
        print(_decode_response(response))

    response_endpoint = _validate_endpoint(server_data["response_endpoint"])
    headers = {"Authorization": f"Bearer {token}"}

    connection.request("GET", url=response_endpoint, headers=headers)
    response = connection.getresponse()
    print(_decode_response(response))

    return response


def _get_connection(server_data):
    host = server_data["host"]
    port = int(server_data["port"])
    timeout = server_data["timeout"]
    context = create_default_context()

    connection = HTTPSConnection(host, port, timeout=timeout, context=context)
    return connection


def _get_token(connection, server_data):
    username = server_data["username"]
    password = server_data["password"]
    headers = {"Content-Type": "application/json"}
    data = dumps({"username": username, "password": password})
    login_endpoint = _validate_endpoint(server_data["login_endpoint"])
    connection.request("POST", url=login_endpoint, body=data, headers=headers)
    response = connection.getresponse()
    token = loads(_decode_response(response))["access_token"]
    return token


def _validate_endpoint(endpoint):
    if not endpoint:
        raise ValueError("Endpoint cannot be empty.")

    if not isinstance(endpoint, str):
        raise TypeError("Endpoint must be a string.")

    splitted_endpoint = endpoint.split("/")
    formatted_endpoint = "/" + "/".join([part for part in splitted_endpoint if part])

    return formatted_endpoint


def _decode_response(response):
    if not response:
        raise ValueError("Response cannot be empty.")

    if not isinstance(response, HTTPResponse):
        raise TypeError("Response must be an instance of http.client.HTTPResponse.")

    return response.read().decode()
