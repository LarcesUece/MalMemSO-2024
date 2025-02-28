import pandas as pd
from flask import current_app as app

from ..models.models import Model
from ..reports.models import Report
from . import db
from .postgres import create_connection


def fetch_data_for_training() -> pd.DataFrame:
    reports = Report.query.filter(Report.file_class != "undefined").all()
    reports_df = pd.DataFrame([report.as_dict() for report in reports])
    return reports_df


def insert_training_data(data: dict) -> None:
    model = Model(**data)
    db.session.add(model)
    db.session.commit()


def is_table_empty(table_name: str) -> bool:
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            return cursor.fetchone()[0] == 0
