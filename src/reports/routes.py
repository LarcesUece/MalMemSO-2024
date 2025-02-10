from flask import current_app as app, request

from ..db import db
from .models import Report
from .utils import get_numeric_columns_average


@app.get("/report/")
def get_reports() -> list:
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    offset = (page - 1) * limit
    reports = Report.query.offset(offset).limit(limit).all()
    return {"reports": [report.as_dict() for report in reports]}


@app.get("/report/count/")
def get_reports_count() -> dict:
    count = Report.query.count()
    return {"reports": count}


@app.get("/report/average/")
def get_reports_average() -> dict:
    return {"reports": get_numeric_columns_average()}


@app.get("/report/<int:id>")
def get_report(id: int) -> dict:
    report = Report.query.get_or_404(id)
    return report.as_dict()


@app.post("/report/")
def post_report() -> dict:
    data = request.json
    report = Report(**data)
    db.session.add(report)
    db.session.commit()
    return report.as_dict()


@app.patch("/report/<int:id>")
def patch_report(id: int) -> dict:
    report = Report.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(report, key, value)
    db.session.commit()
    return report.as_dict()


@app.delete("/report/<int:id>")
def delete_report(id: int) -> dict:
    report = Report.query.get_or_404(id)
    db.session.delete(report)
    db.session.commit()
    return report.as_dict()
