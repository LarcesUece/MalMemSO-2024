import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from flask import current_app as app
from datetime import datetime
import numpy as np
import joblib
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    recall_score,
)
import os
from .db.training import insert_training_data, fetch_data_for_training


def create_model(
    algorithm: str,
) -> (
    DecisionTreeClassifier
    | KNeighborsClassifier
    | MLPClassifier
    | RandomForestClassifier
    | SVC
):
    """Create a model based on the algorithm."""

    if algorithm == "cart":
        return DecisionTreeClassifier()
    elif algorithm == "knn":
        return KNeighborsClassifier(n_neighbors=3)
    elif algorithm == "mlp":
        return MLPClassifier(random_state=1, max_iter=300)
    elif algorithm == "rf":
        return RandomForestClassifier()
    elif algorithm == "svm":
        return SVC(kernel="linear")
    else:
        raise ValueError("Invalid algorithm.")


def train_all(data: pd.DataFrame = None) -> None:
    """Train model for every algorithm available."""

    algorithms = app.config["TRAINING_ALGORITHMS"]

    for algorithm in algorithms:
        app.logger.info(f"Training model for algorithm {algorithm}.")
        model = create_model(algorithm)
        app.logger.info(f"Model created for algorithm {algorithm}.")
        train(model, data)
        app.logger.info(f"Model trained for algorithm {algorithm}.")


def train(
    model: (
        DecisionTreeClassifier
        | KNeighborsClassifier
        | MLPClassifier
        | RandomForestClassifier
        | SVC
    ),
    data: pd.DataFrame = None,
):
    """Normalize the data, split it into training and testing sets, train the model and insert the training details into the model table."""

    if isinstance(model, DecisionTreeClassifier):
        algorithm = "cart"
    elif isinstance(model, KNeighborsClassifier):
        algorithm = "knn"
    elif isinstance(model, MLPClassifier):
        algorithm = "mlp"
    elif isinstance(model, RandomForestClassifier):
        algorithm = "rf"
    elif isinstance(model, SVC):
        algorithm = "svm"
    else:
        raise ValueError("Invalid model.")

    if data is None:
        data = fetch_data_for_training()

    columns_to_drop = ["mem_name_extn", "initial_data", "file_id", "created_at"]

    X = data.copy()
    X = X.drop(columns=columns_to_drop, axis=1)
    class_map = {"benign": 0, "malware": 1}
    X["file_class"] = X["file_class"].map(class_map)
    X = X.dropna()

    Y = X["file_class"]
    X = X.drop("file_class", axis=1)
    X = X.sort_index(axis=1)

    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.3, random_state=1
    )

    app.logger.info("Starting training.")
    init_dt = datetime.now()
    model.fit(X_train, y_train)
    end_dt = datetime.now()
    app.logger.info("Training finished.")
    y_pred = model.predict(X_test)

    training_details = generate_training_details(
        algorithm, model, init_dt, end_dt, y_test, y_pred
    )

    try:
        insert_training_data(training_details)
        app.logger.info("Training details inserted.")
    except Exception as exc:
        raise exc


def generate_training_details(
    algorithm: str,
    model,
    init_dt: datetime,
    end_dt: datetime,
    y_test: np.ndarray,
    y_pred: np.ndarray,
) -> dict:
    """Generate a dictionary with the training details."""

    filename = generate_pickle_filename(algorithm, init_dt)
    pickle_path = os.path.join(app.config["DIR_PICKLE"], filename)
    try:
        joblib.dump(model, filename=pickle_path)
    except Exception:
        raise ("Error while saving the model to a pickle file.")

    try:
        training_details = {
            "algorithm": algorithm,
            "pickle": convert_pickle_to_bytea(pickle_path),
            "pickle_name": filename,
            "train_accuracy": float(accuracy_score(y_test, y_pred)),
            "train_precision": float(average_precision_score(y_test, y_pred)),
            "train_recall": float(recall_score(y_test, y_pred)),
            "train_f1": float(f1_score(y_test, y_pred)),
            "train_init_time": init_dt,
            "train_end_time": end_dt,
            "train_duration": end_dt - init_dt,
        }
    except Exception:
        raise Exception("Error while generating the training details.")

    return training_details


def generate_pickle_filename(algorithm: str, init_dt: datetime):
    """Generate a filename for the pickle file containing the trained model."""

    formatted_dt = init_dt.strftime("%Y%m%d_%H%M%S_%f")
    return f"{algorithm}_{formatted_dt}.pkl"


def convert_pickle_to_bytea(file_path: str) -> bytes:
    """Convert a pickle file to bytea."""

    with open(file_path, "rb") as file:
        return file.read()
