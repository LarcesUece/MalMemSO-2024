from flask import current_app as app
import os
import pandas as pd
from . import db
from .tables import is_table_empty


def insert_initial_data() -> None:
    dir = app.config["INITIAL_DATA_DIR"]
    table_name = app.config["TABLE_ANALYSIS"]

    if not os.path.exists(dir):
        return

    if not is_table_empty(table_name):
        return

    for file in os.listdir(dir):
        if file.endswith(".csv"):
            filepath = os.path.join(dir, file)
            insert_data_from_csv(filepath)


def insert_data_from_csv(file):
    header_mapping = app.config["VOLMEMLYZER_COLUMN_MAPPING"]
    table_name = app.config["TABLE_ANALYSIS"]
    valid_columns = [col for col in header_mapping.values() if col is not None]

    df = pd.read_csv(file)

    filename_options = ["Category", "Filename", "mem.name_extn"]
    if not any(col in df.columns for col in filename_options):
        raise ValueError("CSV file not in expected format.")

    df = df.rename(columns=header_mapping)
    df = df.rename(columns={"Filename": "mem.name_extn"})

    if "analysis_file_class" not in df.columns:
        df["analysis_file_class"] = "malware"

    df = df[valid_columns]

    df.columns = [normalize_column_header(col) for col in df.columns]

    str_columns = df.select_dtypes(include=["object", "string"]).columns
    df[str_columns] = df[str_columns].apply(lambda x: x.str.lower())

    df["initial_data"] = True
    df["file_id"] = None

    df.to_sql(table_name, db.engine, if_exists="append", index=False)
    db.session.commit()


def normalize_column_header(header):
    return header.replace(".", "_").lower()
