from datetime import datetime
from joblib import dump
from numpy import ndarray
from pandas import DataFrame
from pandas.api.types import is_integer_dtype, is_float_dtype, is_datetime64_any_dtype
from pytz import timezone
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    recall_score,
)

import config


def map_pandas_to_postgres(dtype) -> str:
    """Map pandas data types to PostgreSQL data types."""

    if is_integer_dtype(dtype):
        return "INTEGER"
    if is_float_dtype(dtype):
        return "DOUBLE PRECISION"
    if is_datetime64_any_dtype(dtype):
        return "TIMESTAMPTZ"
    return "TEXT"


def generate_create_table_query(
    table_name: str, df: DataFrame = None, columns: list[tuple] = None
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


def get_features_without_correspondence() -> list[str]:
    """Get features that do not have a correspondence in the new version of VolMemLyzer."""

    features_old = config.FEATURES_VOLMEMLYZER_V2
    features_new = config.FEATURES_VOLMEMLYZER_V2_2024

    return [old for old, new in zip(features_old, features_new) if new is None]


def get_timestamp() -> datetime:
    """Get the current timestamp with the timezone specified in the configuration."""

    return datetime.now(timezone(config.PYTZ_TIMEZONE))


def generate_training_details(
    algorithm: str,
    model,
    init_dt: datetime,
    end_dt: datetime,
    y_test: ndarray,
    y_pred: ndarray,
) -> dict:
    """Generate a dictionary with the training details."""

    filename = generate_pickle_filename(algorithm, init_dt)
    dump(model, filename=filename)
    print("Model saved.")

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


def generate_pickle_filename(algorithm: str, init_dt: datetime):
    """Generate a filename for the pickle file containing the trained model."""

    formatted_dt = init_dt.strftime("%Y%m%d_%H%M%S_%f")
    return f"{algorithm}_{formatted_dt}.pkl"


def convert_pickle_to_bytea(file_path: str) -> bytes:
    """Convert a pickle file to bytea."""

    with open(file_path, "rb") as f:
        return f.read()
