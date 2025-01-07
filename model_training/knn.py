from sklearn.neighbors import KNeighborsClassifier
import joblib

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import average_precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from datetime import datetime

from data import normalize_column_header


def train(data: pd.DataFrame):
    X = data.copy()

    columns_to_drop = [
        "callbacks.nanonymous",
        "callbacks.ngeneric",
        "psxview.not_in_csrss_handles",
        "psxview.not_in_csrss_handles_false_avg",
        "psxview.not_in_deskthrd",
        "psxview.not_in_deskthrd_false_avg",
        "psxview.not_in_eprocess_pool",
        "psxview.not_in_eprocess_pool_false_avg",
        "psxview.not_in_ethread_pool",
        "psxview.not_in_ethread_pool_false_avg",
        "psxview.not_in_pslist",
        "psxview.not_in_pslist_false_avg",
        "psxview.not_in_pspcid_list",
        "psxview.not_in_pspcid_list_false_avg",
        "psxview.not_in_session",
        "psxview.not_in_session_false_avg",
        "svcscan.interactive_process_services",
    ]
    columns_to_drop = normalize_column_header(columns_to_drop)

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

    model = KNeighborsClassifier(n_neighbors=3)
    init_dt = datetime.now()
    model.fit(X_train, y_train)
    end_dt = datetime.now()
    diff_dt = end_dt - init_dt

    y_pred = model.predict(X_test)

    print(diff_dt)
    print(accuracy_score(y_test, y_pred))
    print(average_precision_score(y_test, y_pred))
    print(f1_score(y_test, y_pred))
    print(recall_score(y_test, y_pred))

    file_name = "knn_model.pkl"
    joblib.dump(model, file_name)
    return model
