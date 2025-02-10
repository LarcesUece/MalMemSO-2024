from flask import current_app as app
import pandas as pd
from . import db
from .models import Model, Report


def fetch_data_for_training() -> pd.DataFrame:
    reports = Report.query.filter(Report.file_class != "undefined").all()
    reports_df = pd.DataFrame([report.as_dict() for report in reports])
    return reports_df


def insert_training_data(data: dict) -> None:
    model = Model(**data)
    db.session.add(model)
    db.session.commit()
