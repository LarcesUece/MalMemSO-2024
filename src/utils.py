import pandas as pd
import datetime
import pytz
import numpy
from sklearn.metrics import accuracy_score
from sklearn.metrics import average_precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
import sklearn
import joblib
import datetime

import config


def map_pandas_to_postgres(dtype) -> str:
    """Map pandas data types to PostgreSQL data types."""

    if pd.api.types.is_integer_dtype(dtype):
        return "INTEGER"
    if pd.api.types.is_float_dtype(dtype):
        return "DOUBLE PRECISION"
    if pd.api.types.is_datetime64_any_dtype(dtype):
        return "TIMESTAMPTZ"
    return "TEXT"


def generate_create_table_query(
    table_name: str, df: pd.DataFrame = None, columns: list[tuple] = None
) -> str:
    """Generate a CREATE TABLE query for PostgreSQL."""

    if df is not None:
        cols = []
        for col, dtype in df.dtypes.items():
            cols.append(f'"{col}" {map_pandas_to_postgres(dtype)}')
        cols = ", ".join(cols)
    elif columns is not None:
        cols = ", ".join([f'"{col}" {dtype}' for col, dtype in columns])
    else:
        print("No data or columns provided.")
        raise ValueError

    return f"CREATE TABLE {table_name} ({cols});"


def get_features_without_correspondence():
    features_old = config.FEATURES_VOLMEMLYZER_V2
    features_new = config.FEATURES_VOLMEMLYZER_V2_2024

    return [old for old, new in zip(features_old, features_new) if new is None]


def get_timestamp() -> datetime.datetime:
    return datetime.datetime.now(pytz.timezone(config.PYTZ_TIMEZONE))


def generate_training_details(
    algorithm: str,
    model,
    init_dt: datetime.datetime,
    end_dt: datetime.datetime,
    y_test: numpy.ndarray,
    y_pred: numpy.ndarray,
) -> dict:
    filename = generate_pickle_filename(algorithm, init_dt)
    joblib.dump(model, filename=filename)

    return {
        "algorithm": algorithm,
        "model_pickle": convert_pickle_to_bytea(filename),
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(average_precision_score(y_test, y_pred)),
        "recall": float(recall_score(y_test, y_pred)),
        "f1": float(f1_score(y_test, y_pred)),
        "init_time": init_dt,
        "end_time": end_dt,
        "training_duration": end_dt - init_dt,
    }


def generate_pickle_filename(algorithm: str, init_dt: datetime.datetime):
    formatted_dt = init_dt.strftime("%Y%m%d_%H%M%S_%f")
    return f"{algorithm}_{formatted_dt}.pkl"


def convert_pickle_to_bytea(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        return f.read()
