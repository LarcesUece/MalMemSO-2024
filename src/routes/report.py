from flask import current_app as app, request
from ..db.models import Report
from ..db import db


@app.get("/report/")
def list_reports() -> list:
    reports = Report.query.limit(10).all()
    return [report.as_dict() for report in reports]


@app.get("/report/info/")
def get_reports_info() -> dict:
    count = Report.query.count()
    return {"reports": count}


@app.post("/report/")
def post_report() -> dict:
    data = request.json
    report = Report(**data)
    db.session.add(report)
    db.session.commit()
    return report.as_dict()


@app.get("/report/<int:id>")
def get_report(id: int) -> dict:
    report = Report.query.get_or_404(id)
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
