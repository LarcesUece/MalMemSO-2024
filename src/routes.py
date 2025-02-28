from flask import current_app as app
from flask import send_from_directory
from flask.typing import ResponseReturnValue
from flask.wrappers import Response
from werkzeug.exceptions import HTTPException

from .utils import format_error_message


@app.route("/")
def root() -> ResponseReturnValue:
    return {"message": "MalMemSO is running."}


@app.route("/favicon.ico")
def favicon() -> ResponseReturnValue:
    return send_from_directory(
        directory=app.static_folder,
        path="favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.errorhandler(HTTPException)
def handle_exception(exception: HTTPException) -> ResponseReturnValue:
    return {"error": format_error_message(exception.name)}, exception.code
