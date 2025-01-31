from flask import current_app as app, request
from ..db.models import Analysis
from ..db import db


@app.get("/analysis/")
def list_analysiss() -> list:
    analyses = Analysis.query.limit(10).all()
    return [analysis.as_dict() for analysis in analyses]


@app.get("/analysis/info/")
def get_analyses_info() -> dict:
    analyses = Analysis.query.all()
    return {"analyses": len(analyses)}


@app.post("/analysis/")
def post_analysis() -> dict:
    data = request.json
    analysis = Analysis(**data)
    db.session.add(analysis)
    db.session.commit()
    return analysis.as_dict()


@app.get("/analysis/<int:id>")
def get_analysis(id: int) -> dict:
    analysis = Analysis.query.get_or_404(id)
    return analysis.as_dict()


@app.patch("/analysis/<int:id>")
def patch_analysis(id: int) -> dict:
    analysis = Analysis.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(analysis, key, value)
    db.session.commit()
    return analysis.as_dict()


@app.delete("/analysis/<int:id>")
def delete_analysis(id: int) -> dict:
    analysis = Analysis.query.get_or_404(id)
    db.session.delete(analysis)
    db.session.commit()
    return analysis.as_dict()
