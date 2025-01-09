from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

import config
import db
import utils


def initialize() -> None:
    """Initialize the model table and train the models."""

    db.create_table(config.MODEL_TABLE, columns=config.MODEL_COLUMNS)
    if not db.table_has_data(config.MODEL_TABLE):
        train_all()


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
        print("Invalid algorithm.")
        raise ValueError


def train_all(data: DataFrame = None) -> None:
    """Train model for every algorithm available."""

    for algorithm in config.ALGORITHMS:
        model = create_model(algorithm)
        train(model, data)


def train(
    model: (
        DecisionTreeClassifier
        | KNeighborsClassifier
        | MLPClassifier
        | RandomForestClassifier
        | SVC
    ),
    data: DataFrame = None,
):
    """Train the model and insert the training details into the model table."""

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
        print("Invalid model.")
        raise ValueError

    if not data:
        data = db.fetch_data(config.DATA_TABLE)

    X = data.copy()

    columns_to_drop = utils.get_features_without_correspondence()
    X = X.drop(columns=columns_to_drop, axis=1)
    X = X.drop("Category", axis=1)
    class_map = {"Benign": 0, "Malware": 1}
    X["Class"] = X["Class"].map(class_map)
    Y = X["Class"]
    X = X.drop("Class", axis=1)
    X = X.sort_index(axis=1)

    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.3, random_state=1
    )

    init_dt = utils.get_timestamp()
    model.fit(X_train, y_train)
    end_dt = utils.get_timestamp()
    y_pred = model.predict(X_test)
    print(f"Model trained for {algorithm}.")

    training_details = utils.generate_training_details(
        algorithm, model, init_dt, end_dt, y_test, y_pred
    )

    try:
        db.insert_data(config.MODEL_TABLE, data=training_details)
        print(f"Training details for {algorithm} inserted successfully.")
    except Exception:
        print("Error while inserting training details.")
        raise
