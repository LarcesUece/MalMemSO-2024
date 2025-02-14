from configparser import SectionProxy
from http.client import (
    ResponseNotReady,
    CannotSendRequest,
    HTTPSConnection,
    HTTPResponse,
)
from json import loads
from logging import error, info
from time import sleep

from modules import get_response
from utils import get_connection, get_token, validate_endpoint, decode_response

import unittest


class TestResponseGetter(unittest.TestCase):
    def setUp(self):
        self.filename = "filename.zip"
        self.server_data = {
            "username": "username",
            "password": "password",
            "host": "host",
            "port": "port",
            "timeout": 3600,
        }
        self.endpoint_data = {
            "login": "login",
            "upload": "upload",
            "response": "response",
        }
        self.mock_response_data = {"filename": self.filename, "result": "success"}

        self.original_get_connection = get_connection
        self.original_get_token = get_token
        self.original_validate_endpoint = validate_endpoint
        self.original_decode_response = decode_response

    def tearDown(self):
        global get_connection, get_token, validate_endpoint, decode_response

        get_connection = self.original_get_connection
        get_token = self.original_get_token
        validate_endpoint = self.original_validate_endpoint
        decode_response = self.original_decode_response

    def mock_get_connection(self, server_data):
        mock_connection = unittest.mock.Mock(spec=HTTPSConnection)
        mock_response = unittest.mock.Mock(spec=HTTPResponse)

        mock_response.status = 200
        mock_response.read.return_value = (
            b'{"filename": "filename.zip", "result": "success"}'
        )
        mock_connection.getresponse.return_value = mock_response

        return mock_connection

    def mock_get_token(self, connection, server_data, endpoint_data):
        return "mock_token"

    def mock_validate_endpoint(self, endpoint):
        return "/mock-response-endpoint"

    def mock_decode_response(self, response):
        return {"filename": "filename.zip", "result": "success"}


if __name__ == "__main__":
    unittest.main()
