from flask import current_app as app, request
from threading import Thread

from ..db import db
from ..db.models import File
from ..training import train_all


@app.get("/file/")
def get_files() -> list:
    files = File.query.all()
    return {"files": [file.as_dict() for file in files]}


@app.get("/file/count/")
def get_files_count() -> dict:
    count = File.query.count()
    return {"files": count}


@app.get("/file/<int:id>")
def get_file(id: int) -> dict:
    file = File.query.get_or_404(id)
    return {"file": file.as_dict()}


@app.post("/file/")
def post_file() -> dict:
    if "file" not in request.files:
        return {"error": "No file part."}, 400

    file = request.files["file"]
    if file.filename == "":
        return {"error": "No selected file."}, 400

    if not file.filename.endswith(".zip"):
        return {"error": "Invalid file extension."}, 400

    data = request.json
    file = File(**data)
    db.session.add(file)
    db.session.commit()

    return {"file": file.as_dict()}, 201


@app.patch("/file/<int:id>")
def patch_file(id: int) -> dict:
    file = File.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(file, key, value)
    db.session.commit()
    return {"file": file.as_dict()}


@app.delete("/file/<int:id>")
def delete_file(id: int) -> dict:
    file = File.query.get_or_404(id)
    db.session.delete(file)
    db.session.commit()
    return "", 204
