from sqlalchemy.sql.sqltypes import Float, Integer, Numeric
from sqlalchemy.sql import func

from .models import Report
from ..db import db


def get_numeric_columns_average() -> dict:
    numeric_columns = [
        column
        for column in Report.__table__.columns
        if isinstance(column.type, (Numeric, Integer, Float))
        and not column.name in ["id", "file_id"]
    ]

    avg_expressions = [
        func.avg(column).label(f"{column.name}_avg") for column in numeric_columns
    ]

    averages = db.session.query(*avg_expressions).first()
    average_dict = (
        {column.name: avg for column, avg in zip(numeric_columns, averages)}
        if averages
        else {}
    )

    return average_dict
