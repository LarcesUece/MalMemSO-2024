from flask import current_app as app, jsonify
from ..db.models import Analysis


@app.get("/analysis/")
def list_analysiss():
    analyses = Analysis.query.limit(10).all()
    return jsonify([analysis.as_dict() for analysis in analyses])


@app.post("/analysis/")
def post_analysis():
    return "Post analysis."


@app.get("/analysis/<int:id>")
def get_analysis(id: int):
    return f"Get analysis {id}."


@app.patch("/analysis/<int:id>")
def patch_analysis(id: int):
    return f"Patch analysis {id}."


@app.delete("/analysis/<int:id>")
def delete_analysis(id: int):
    return f"Delete analysis {id}."
