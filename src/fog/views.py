from datetime import datetime
from flask import jsonify, request
from flask.views import MethodView
from multiprocessing import Process
from os.path import join

from app import app
from src import report, zip


class ZIPView(MethodView):
    def __init__(self):
        self.methods = ["POST"]
        self.zip_dir = app.config.get("ZIP_DIR")
        self.timestamp_format = app.config.get("TIMESTAMP_FORMAT")

    def post(self):
        if "file" not in request.files:
            return jsonify({"error": "No file part."}), 400

        file = request.files["file"]
        received_at = datetime.now().strftime(self.timestamp_format)

        if file.filename == "":
            return jsonify({"error": "No selected file."}), 400

        if not file.filename.endswith(".zip"):
            return jsonify({"error": "Invalid file extension."}), 400

        file_id = report.generate_file_id()
        file_path = join(self.zip_dir, file_id + ".zip")
        file.save(file_path)

        report.update_report(file_id, received_at=received_at, status="saved")

        process = Process(target=zip.process_zip_file, args=(file_path, file_id))
        process.start()

        return jsonify({"file_id": file_id}), 201


class IDView(MethodView):
    def __init__(self):
        self.methods = ["GET"]
        self.report_file = app.config.get("REPORT_FILE")

    def get(self, file_id):
        data, status_code = report.get_report(file_id)
        return jsonify(data), status_code


app.add_url_rule("/zip/", view_func=ZIPView.as_view("zip"))
app.add_url_rule("/id/<file_id>/", view_func=IDView.as_view("id"))
