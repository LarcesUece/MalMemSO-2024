from flask import current_app as app
from flask import jsonify, request
from threading import Thread

from config import DATA_TABLE, DATA_COLUMNS_NAMES
from db import insert_data, fetch_data, delete_table
from model import train_all


@app.errorhandler(404)
def not_found(e):
    return "The resource you are looking for does not exist.", 404


@app.route("/")
def index():
    return "MalMemSO Cloud is running."


@app.post("/data")
def receive_data():
    """Receive data, validate, insert it into the data table and start a thread to train the models."""

    try:
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "No data provided."}), 400

        validated_data = {}

        for feature in request_data:
            if feature in DATA_COLUMNS_NAMES:
                validated_data[feature] = request_data[feature]

        missing_features = []

        for feature in DATA_COLUMNS_NAMES:
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

        return jsonify({"message": "Data received and inserted successfully."}), 201
    except Exception as err:
        return jsonify({"error": str(err)}), 500


# Debug function
# @app.get("/data")
# def get_last_data():
#     try:
#         data = fetch_data(DATA_TABLE, 5, True)
#         return jsonify(data.to_dict(orient="records"))
#     except Exception as err:
#         return jsonify({"error": str(err)}), 500

# Debug function
# @app.get("/delete/data")
# def delete_table_data():
#     try:
#         delete_table(DATA_TABLE)
#         return jsonify({"message": "Data deleted."})
#     except Exception as err:
#         return jsonify({"error": str(err)}), 500
