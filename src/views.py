from flask import current_app as app
from flask.views import MethodView


class File(MethodView):
    def get(self, id):
        if id is None:
            return "GET file"
        return f"GET file {id}"

    def post(self):
        return "POST file"


dump_view = File.as_view("file")
app.add_url_rule("/file/", view_func=dump_view, methods=["GET", "POST"])
app.add_url_rule("/file/<int:id>", view_func=dump_view, methods=["GET"])
