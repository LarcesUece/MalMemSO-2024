from flask import current_app as app, send_from_directory
from werkzeug.exceptions import HTTPException
from ..utils import format_error_message


@app.route("/")
def root():
    return ({"message": "MalMemSO is running."}, 200)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        app.static_folder, "favicon.ico", mimetype="image/vnd.microsoft.icon"
    )


@app.errorhandler(HTTPException)
def handle_exception(exception):
    return ({"error": format_error_message(exception.name)}, exception.code)
