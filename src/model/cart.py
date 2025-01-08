from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from sklearn.model_selection import train_test_split

import db
import utils
import config


def train(data: pd.DataFrame) -> None:
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

    model = DecisionTreeClassifier()
    init_dt = utils.get_timestamp()
    model.fit(X_train, y_train)
    end_dt = utils.get_timestamp()

    y_pred = model.predict(X_test)

    algorithm = "cart"
    training_details = utils.generate_training_details(
        algorithm, model, init_dt, end_dt, y_test, y_pred
    )

    db.insert_data_to_postgres(config.MODEL_TABLE, data=training_details)
