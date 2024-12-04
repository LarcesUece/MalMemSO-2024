from flask import Flask, request, jsonify
import os

# from .fog import routes
from .utils import setup_argparser, setup_logging

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Malware Detection: Fog module"


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = os.path.join("uploads", file.filename)
        file.save(filename)

        return jsonify({"message": "File uploaded successfully"}), 200

    return jsonify({"error": "Something went wrong"}), 500


if __name__ == "__main__":
    setup_logging()
    args = setup_argparser()
