import os

import pandas as pd
from flask import current_app as app

from . import db
from .utils import is_table_empty


def insert_initial_data() -> None:
    dir = app.config.get("DIR_INITIAL_DATA")
    table_name = app.config.get("TABLE_REPORT")

    if not os.path.exists(dir):
        return

    if not is_table_empty(table_name=table_name):
        return

    for file in os.listdir(dir):
        if file.endswith(".csv"):
            filepath = os.path.join(dir, file)
            insert_data_from_csv(filepath=filepath)


def insert_data_from_csv(filepath: str) -> None:
    header_mapping = app.config.get("VOLMEMLYZER_COLUMN_MAPPING")
    table_name = app.config.get("TABLE_REPORT")
    valid_columns = [col for col in header_mapping.values() if col is not None]

    df = pd.read_csv(filepath_or_buffer=filepath)

    filename_options = ["Category", "Filename", "mem.name_extn"]
    if not any(col in df.columns for col in filename_options):
        raise ValueError("CSV file not in expected format.")

    df = df.rename(columns=header_mapping)
    df = df.rename(columns={"Filename": "mem.name_extn"})

    if "report_file_class" not in df.columns:
        df["report_file_class"] = "malware"

    df = df[valid_columns]

    df.columns = [normalize_column_header(header=col) for col in df.columns]

    str_columns = df.select_dtypes(include=["object", "string"]).columns
    df[str_columns] = df[str_columns].apply(lambda x: x.str.lower())

    df["initial_data"] = True
    df["dump_id"] = None

    df.to_sql(name=table_name, con=db.engine, if_exists="append", index=False)
    db.session.commit()


def normalize_column_header(header: str) -> str:
    normalized_header = header.replace(".", "_").lower()
    return normalized_header
