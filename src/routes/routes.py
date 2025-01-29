from flask import current_app as app, render_template, jsonify


@app.route("/")
def root():
    content = "MalMemSO service is running."
    return render_template("default.html", content=content)


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": error.name}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": error.name}), 405


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": error.name}), 500
