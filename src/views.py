from app import app
from flask import request, jsonify
from flask.views import View
from src import volmemlyzer
import uuid
import os
import threading


class CSVView(View):
    def __init__(self):
        self.csv_dir = app.config["CSV_DIR"]

    def dispatch_request(self):
        return "CSV View"

    def get(self):
        return "CSV View GET"


class RAWView(View):
    def __init__(self):
        self.raw_dir = app.config["RAW_DIR"]

    def dispatch_request(self):
        return "RAW View"

    def get(self):
        return "RAW View GET"

    def post(self):
        return "RAW View POST"


class ZIPView(View):
    def __init__(self):
        self.zip_dir = app.config["ZIP_DIR"]

    def dispatch_request(self):
        return "ZIP View"

    def get(self):
        return "ZIP View GET"

    def post(self):
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if not file.filename.endswith(".zip"):
            return jsonify({"error": "Invalid file extension"}), 400

        file_id = str(uuid.uuid4())
        file_path = os.path.join(self.zip_dir, file_id + ".zip")
        file.save(file_path)

        thread = threading.Thread(target=volmemlyzer.run)
        thread.start()

        return jsonify({"id": file_id}), 201


app.add_url_rule("/csv/", view_func=CSVView.as_view("csv"))
app.add_url_rule("/raw/", view_func=RAWView.as_view("raw"))
app.add_url_rule("/zip/", view_func=ZIPView.as_view("zip"))
