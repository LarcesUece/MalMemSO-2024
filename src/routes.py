from flask import current_app as app
from flask import jsonify, request
from threading import Thread

from config import DATA_TABLE, FEATURES_VOLMEMLYZER_V2
from db import insert_data
from model import train_all


@app.errorhandler(404)
def not_found(e):
    return "The resource you are looking for does not exist.", 404


@app.route("/")
def index():
    return "MalMemSO Cloud is running."


@app.post("/data")
def receive_data():
    try:
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "No data provided."}), 400

        validated_data = {}

        for feature in request_data:
            if feature in FEATURES_VOLMEMLYZER_V2:
                validated_data[feature] = request_data[feature]

        missing_features = []

        for feature in FEATURES_VOLMEMLYZER_V2:
            if not feature in validated_data:
                missing_features.append(feature)

        if len(missing_features) > 0:
            return (
                jsonify(
                    {
                        "error": f"Missing {len(missing_features)} features in the data received: {missing_features}"
                    }
                ),
                400,
            )

        insert_data(DATA_TABLE, data=validated_data)

        thread = Thread(target=train_all)
        thread.start()

        return jsonify({"message": "Data received."}), 201
    except Exception as err:
        return jsonify({"error": str(err)}), 500
