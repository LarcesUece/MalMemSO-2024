from flask import current_app as app
import pandas as pd
from . import db
from .models import Model, Analysis


def fetch_data_for_training() -> pd.DataFrame:
    analyses = Analysis.query.filter(Analysis.file_class != "undefined").all()
    analyses_df = pd.DataFrame([analysis.as_dict() for analysis in analyses])
    return analyses_df


def insert_training_data(data: dict) -> None:
    model = Model(**data)
    db.session.add(model)
    db.session.commit()
