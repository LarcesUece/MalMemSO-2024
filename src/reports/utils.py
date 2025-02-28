from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Float, Integer, Numeric

from ..db import db
from .models import Report


def get_numeric_columns_average() -> dict:
    numeric_columns = [
        column
        for column in Report.__table__.columns
        if isinstance(column.type, (Numeric, Integer, Float))
        and not column.name in ["id", "dump_id"]
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
