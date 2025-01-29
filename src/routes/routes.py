from flask import current_app as app


@app.route("/")
def root():
    return "MalMemSO service is running."


@app.errorhandler(404)
def page_not_found(e):
    return "Not found.", 404


@app.errorhandler(405)
def method_not_allowed(e):
    return "Not allowed.", 405


@app.errorhandler(500)
def internal_server_error(e):
    return "Internal server error. Try again.", 500
